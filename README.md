# aml-pipeline-CommandStep
A small example to illustrate the Command Step as part of Azure Machine Learning's pipelines. In this example,
two basic R scripts are run in two steps of a pipeline. They just do a simple data transformation in each R
script, but illustrate how inputs and outputs flow between pipeline steps. A `Makefile` helps showcase the
steps in running the various scripts. Authentication is handled through a service principal. Before initiating
the `create-workspace-sprbac.sh`, ensure there is a file called `sub.env`, which has the following one line
detail: `SUB_ID=<your subscription ID>`.
