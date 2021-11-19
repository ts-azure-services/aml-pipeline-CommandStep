import os
from pathlib import Path
from azureml.core import Dataset
from azureml.core import Experiment, ScriptRunConfig
from authentication import ws

# Filepaths
target_def_blob_store_path = '/blob-input-data/'
output_def_blob_store_path = '/sample/outputs/'
local_data_folder = './input-data/'

# Define some functions to be used below
def data_filepaths(data_folder=None):
    """Get full paths to discrete data files"""
    full_filepaths = []
    absolute_path = Path(data_folder).absolute()
    data_files = os.listdir(data_folder)
    for file in data_files:
        file_with_path = str(absolute_path) + '/' + str(file)
        full_filepaths.append(file_with_path)
    return full_filepaths


def create_dataset(default_ds=None, input_data_source=None, workspace=None, name=None, tags=None, file_type='file'):
    """Create dataset from input data files"""
    try:
        if file_type=="file":
            dset= Dataset.File.from_files(path=(default_ds, input_data_source))
        elif file_type=="tabular":
            dset= Dataset.Tabular.from_delimited_files(path=(default_ds, input_data_source))
    except Exception as e:
        print(e)
    return dset


def register_dataset(dataset=None, workspace=None, name=None, desc=None,tags=None):
    """Register datasets"""
    try:
        dataset = dataset.register(workspace=workspace, name=name, description=desc, tags=tags,create_new_version=True)
        print(f" Dataset registration successful for {name}")
    except Exception as e:
        print(f" Exception in registering dataset. Error is {e}")

# Get input data files from local
data_file_paths = data_filepaths(data_folder = local_data_folder)

# Get the default blob store
def_blob_store = ws.get_default_datastore()

# Upload files to blob store
def_blob_store.upload_files(
    files=data_file_paths, 
    target_path=target_def_blob_store_path,
    overwrite=True,
    show_progress=True
)

# Create the dataset from the datastore
fd = create_dataset(
    default_ds = def_blob_store,
    input_data_source=target_def_blob_store_path, 
    workspace=ws, 
    name="Sample Diabetes File - Take 4",
    tags={'format':'CSV'},
    file_type='file'
)

register_dataset(dataset=fd, workspace=ws, name='file_dataset')
