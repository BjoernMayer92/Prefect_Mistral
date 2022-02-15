import prefect
from prefect import task, Flow, unmapped
import xarray as xr

import xarray as xr
import pathlib
import os
import numpy as np
import argparse
from prefect.engine.executors import DaskExecutor

parser = argparse.ArgumentParser()
parser.add_argument("--cluster", type=str)
parser.add_argument("--project", type=str)
parser.add_argument("--run", default = False, type=bool)
args = parser.parse_args()

cluster_address = args.cluster
project = args.project
run = args.run

print(cluster_address)

from dask.distributed import Client



proj_dir = pathlib.Path.cwd().resolve().parents[0]
data_dir = os.path.join(proj_dir, "data")
data_raw_dir = os.path.join(data_dir, "raw")
data_pro_dir = os.path.join(data_dir, "processed")

if not os.path.exists(data_pro_dir):
    os.makedirs(data_pro_dir)
if not os.path.exists(data_raw_dir):
    os.makedirs(data_raw_dir)




logger = prefect.context.get("logger")

n_files = 10

@task
def create_data(size, n_files):
    logger.info("create data started")
    filepaths = []
    for file_index in range(n_files):
        logger.info("filen index {} started".format(file_index))
        data = xr.DataArray(np.random.normal(size=size), dims = ["time","lat","lon"])
        logger.info("data {} created".format(file_index))
        filepath = os.path.join(data_raw_dir,"data_{}.nc".format(file_index))
        filepaths.append(filepath)
        data.to_netcdf(filepath)
        logger.info("data {} saved".format(file_index))
        
    return filepaths

@task 
def make_mean(filepath,dims):
    data = xr.load_dataset(filepath)
    data_mean = data.mean(dim=dims)
    filename = os.path.basename(filepath)
    data_mean.to_netcdf(os.path.join(data_pro_dir,filename))

dask_executor = DaskExecutor(address = cluster_address)
with Flow("mistral_test", executor = dask_executor) as flow:
    filepaths = create_data(size = (10**3,10**2,10**2), n_files=10)
    make_mean.map(filepaths,unmapped(("lat","lon")))

if run == False:
    flow.register(project_name = project)
if run ==True:
    flow.run()
