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

- api server
    - load persisted model
    - serve requests to model

to ensure stable builds, using poetry to control all libraries.

# Containers

four main, different uses:

- load data
    - mostly I/O, may be external internet not much memory or cpu
    - external internet/ credentials
        - higher security

- configure data
    - local I/O, may be high cpu (depending on changes/features)

- train model
    - heavy compute, may be heavy memory, also I/O

- model api server
    - depending on use case;  medium compute/memory, may be high I/O ?
    - may be external facing
        - higher security

using graphviz .dot format for diagrams, and a cli version of sketchviz
