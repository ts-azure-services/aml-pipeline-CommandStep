install:
	#pip install --upgrade pip && pip install -r requirements.txt
	./create-workspace-sprbac.sh

setup:
	python create_cluster.py
	python create_env.py
	python datasets.py

pipeline:
	python mock_pipeline.py

all: install setup
