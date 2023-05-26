notes
-----

steps in the process

![steps](./steps.svg)

# Jupyter Notebooks
initial experiments using jupyter notebooks.
[sample](../notebooks/)

once code is mostly correct, proceed to write in pure python
resulting in

# Cleaned Python

![python](./python_flow.svg)

- credentials
    - credential handling depends on environment.  For this example need the kaggle.json file with username and key. (don't want to put those into a public repository)

- config file
    - contains local paths
    - logging config
    - data source location

- initial setup
    - check and create required directories if needed

- get data
    - download data and store locally

- configure data
    - etl step, convert the csv to parquet, and create feature data

- train model
    - train model on given data
    - persist model to local drive
    - run tests

- run model
    - load persisted model
    - run tests

to ensure stable builds, using poetry to control all libraries.

# Containers

three main, different uses:

- load data
    - mostly I/O, not much memory or cpu

- train model
    - heavy compute, may be heavy memory, also I/O

- server model
    - depending on use case;  medium compute/memory, may be high I/O ?

using graphviz .dot format for diagrams, and a cli version of sketchviz
