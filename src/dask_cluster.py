import prefect
from prefect import task, Flow
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
args = parser.parse_args()

cluster_address = args.cluster
project = args.project

print(cluster_address)

from dask.distributed import Client



proj_dir = pathlib.Path.cwd().resolve().parents[0]
data_dir = os.path.join(proj_dir, "data")
data_raw_dir = os.path.join(data_dir, "raw")
data_pro_dir = os.path.join(data_dir, "processed")

print(proj_dir)
print(data_dir)
if not os.path.exists(data_pro_dir):
    os.makedirs(data_pro_dir)



logger = prefect.context.get("logger")


@task
def create_data(size):
    data = xr.DataArray(np.random.normal(size=size))
    data.to_netcdf("test.nc")


dask_executor = DaskExecutor(address = cluster_address)
with Flow("mistral_test", executor = dask_executor) as flow:
    create_data((10**3,10**3,10**3))

flow.register(project_name = project)
