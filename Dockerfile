FROM continuumio/miniconda3:4.6.14
RUN apt-get update && yes Y | apt-get install build-essential
RUN conda install -c r r-essentials r-argparse r-reticulate r-proc r-stringr r-rpart r-caret
