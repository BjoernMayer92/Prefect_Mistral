import logging
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import argparse

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument("--name", type=str, help = "Name of the job which appears in Slurm", default ="dask-cluster")
parser.add_argument("--partition", type=str, help="Name of the partition where the job will run", default = "shared", choices = ["shared", "prepost"])
parser.add_argument("--project", type=str, help = "Name of the project")
parser.add_argument("--cores", type=int, help="Number of cores")
parser.add_argument("--interface", type=str, default = "ib0")
parser.add_argument("--memory", type = str, help = "Size of memory reserved")
parser.add_argument("--workers", type= int, help = "Number of workers")
parser.add_argument("--port", type=int, default = 8080, help = "Portnumber for dashboard") 
parser.add_argument("--walltime", type=str, default = "8:00:00", help="Walltme for each individual worker")
args = parser.parse_args()

name = args.name
queue = args.partition
project = args.project
cores = args.cores
interface = args.interface
memory = args.memory
workers = args.workers
port=args.port
walltime=args.walltime

cluster = SLURMCluster(name=name, queue = queue, project= project, cores=cores, interface=interface, memory=memory, walltime = walltime, scheduler_options={"dashboard_address": ":{}".format(str(port))})
client = Client(cluster)

cluster.scale(workers)

logging.info(client)
input("Press enter to close cluster")
