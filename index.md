## Welcome to GitHub Pages
Guide on how to run prefect workflows on a dask slurmcluster deployed on Mistral from DKRZ ([Link](https://docs.dkrz.de/doc/mistral/index.html)) 



# Setting up Slurm Cluster

Use either [jupyterhub](https://jupyterhub.dkrz.de/) to start a dask slurm cluster or run it as a [script](./src/start_slurmcluster.py) on mistral directly. Since compute nodes do not have internet access, only shared and prepost are availiable. For more info check [Link](https://docs.dkrz.de/blog/2020/dask_jobqueue.html)
```markdown
cluster = SLURMCluster(name=name,
                       queue = queue,
                       project= project,
                       cores=cores, 
                       interface=interface,
                       memory=memory,
                       walltime = walltime,
                       scheduler_options={"dashboard_address": ":{}".format(str(port))})

client = Client(cluster)

cluster.scale(workers)
```
When using jupyterhub you should be able to view the dashboard directly in the browser. When running a cluster in the terminal you need to forward the port via ssh tunneling to your local PC and should then be able to view the dask dashboard. Save the cluster address since we need to connect our job to the cluster in a later step.

The output of client should look similar to this:

![Image](./docs/assets/images/dask_scheduler.png)

# Setting up Prefect
## Set up the prefect cloud
Setting up the prefect cloud follows this tutorial [Link](https://docs.prefect.io/orchestration/getting-started/set-up.html#set-the-prefect-cloud-backend)
### Set the prefect cloud backend
```markdown
prefect backend cloud
```
### Login in
For this example we will use the cloud solution provided by prefect. But also setting up your own prefect server will work. First we need to create an account and log in to
https://cloud.prefect.io/
### Setting up the API key
For authentication we will need to generate an authentication key here : [Link](https://cloud.prefect.io/user/keys). The newly created key will be copied and stored for use by:
```markdown
prefect auth login --key <YOUR-KEY>
```
### Create a new projects
```markdown
prefect create project "tutorial"
```
## Register a flow
We can now register a flow for this project with the general structure of prefect:
```markdown
from prefect.engine.executors import DaskExecutor

dask_executor = DaskExecutor(address = cluster_address)
with Flow("mistral_test", executor = dask_executor) as flow:
    flow.register(project_name = project)

```
Here cluster address is the address of our Slurm cluster set up at the beginning and project the name of our porject ("tutorial"). An example script can be found [here](./src/prefect_pipeline.py) and run via the following command:
```markdown
    python prefect_pipeline.py --cluster=<cluster_address> --project="tutorial"

```
The registered flow in the cloud should now be visible:
![Image](./docs/assets/images/Prefect_flow.png)

## Register an Agent
Finally we need to register mistral as an agent for our workflow. This can be done in one line:
``` markdown
    prefect agent local start

```
The output of the command should look like this:
![Image](./docs/assets/images/Prefect_agent.png)

### Running the flow
After the setup your flow should show the registered agent on the left side:
![Image](./docs/assets/images/Prefect_registered.png)
You can now click quick run

### Supervision of the FLow
You can supervise your Flow in the dask cluster as well as on the prefect cloud:

https://user-images.githubusercontent.com/63497217/154149940-a99c01ed-71ae-48f7-a554-49a566b910de.mp4



https://user-images.githubusercontent.com/63497217/154150948-e37e44e4-3c5c-4d20-82db-086b02b7386e.mp4

