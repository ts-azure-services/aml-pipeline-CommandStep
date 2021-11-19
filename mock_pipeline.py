from azureml.core import Dataset, Environment, Workspace, ScriptRunConfig
from azureml.core.experiment import Experiment
from azureml.core.compute import ComputeTarget
from azureml.pipeline.steps import CommandStep
from azureml.pipeline.core import Pipeline
from azureml.data import OutputFileDatasetConfig
from authentication import ws

# Pipeline step 1: Cleanup file
def_blob_store = ws.get_default_datastore()
ds = Dataset.get_by_name(workspace=ws, name='file_dataset')
compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
env= Environment.get(workspace=ws, name='new_env')
experiment = Experiment(ws, 'exp1')
intermediate_source = OutputFileDatasetConfig(destination=(def_blob_store,'/inter/')).as_mount()
final_source = OutputFileDatasetConfig(destination=(def_blob_store,'/inter/')).as_mount()


# First pipeline step
R_script = 'first_process.R'
first_src = ScriptRunConfig(
        source_directory='./RSCRIPTS',
        command=[
            'Rscript',R_script, # local file
            '--input_file_path', ds.as_named_input('starting').as_mount(),
            '--output_file_path', intermediate_source,
            ],
        environment=env)
first_step = CommandStep(name='first_step',runconfig=first_src, compute_target=compute_target)

# Second pipeline step
R_script = 'second_process.R'
second_src = ScriptRunConfig(
        source_directory='./RSCRIPTS',
        command=[
            'Rscript',R_script, # local file
            '--input_file_path', intermediate_source.as_input(),
            '--output_file_path',final_source,
            ],
        environment=env)
second_step = CommandStep(name='second_step',runconfig=second_src, compute_target=compute_target)

# Pipeline integration
steps = [ first_step, second_step ]
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline_run = experiment.submit(pipeline)
pipeline_run.wait_for_completion()

# Publish the pipeline
published_pipeline = pipeline.publish('Final_pipeline')
