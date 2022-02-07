## Welcome to GitHub Pages
Guide on how to run prefect workflows on a dask slurmcluster deployed on Mistral from DKRZ ([Link](https://docs.dkrz.de/doc/mistral/index.html)) 

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for


1. Start a dask Slurmcluster.

    Use either jupyterhub([Link](https://jupyterhub.dkrz.de/)) to start a dask slurm cluster or run it as a script on mistral directly. For more info check [Link](https://docs.dkrz.de/blog/2020/dask_jobqueue.html)
```markdown
from dask_jobqueue import SLURMCluster
from dask.distributed import Client

cluster = SLURMCluster(name="dask-cluster", queue ="shared", project="uo1075", cores=12, interface="ib0", memory="16GB")
client = Client(cluster)

cluster.scale(4)
```
The output of client should look similar to this:
[Img]()

3. List

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List


**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/BjoernMayer92/Prefect_Mistral/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
