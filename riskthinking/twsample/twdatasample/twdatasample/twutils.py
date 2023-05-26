#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import yaml
import logging
import os


def getconfig(configfile="/twdata/data_config.yml"):
    config = {}
    # get config in global space
    with open(configfile, "r") as stream:
        try:
            # Converts yaml document to python object
            config = yaml.safe_load(stream)
            # Printing dictionary
            if config["logging"]["debuglevel"] > 0:
                print(config)
        except yaml.YAMLError as e:
            print(e)

    # test config here
    # check dirs exist
    # check values

    return config


def checkconfig(configfile="/twdata/data_config.yml"):
    # hard coding
    # check if config is valid
    # check if config dirs exist
    #   warn and create if not
    #    slight "chicken and egg for logging"
    config = getconfig(configfile)
    dirchecklist = {
        "kaggledir": config["data"]["kaggle"],
        "parquedir": config["data"]["parquet"],
        "modeldir": config["data"]["modeldir"],
        "featuredir": config["data"]["featuredir"],
        "logdir": config["logging"]["logdir"],
    }

    for d in dirchecklist.keys():
        if os.path.exists(dirchecklist[d]) == False:
            print(f"dir for {d}{dirchecklist[d]} does not exist, creating")
            os.makedirs(dirchecklist[d])
            logging.warn(f"dir for {d} does not exist, creating")
        else:
            print(f"dir for {d}{dirchecklist[d]} exists")


def setuplogging(config):
    logfile = config["logging"]["logdir"] + "/" + config["logging"]["logfile"]
    logformat = config["logging"]["format"]

    logging.basicConfig(
        filename=logfile, filemode="a", level=logging.DEBUG, format=logformat
    )
    logger = logging.getLogger("tw logger")
    return logger


def splitjobdump(model, config):
    # Define the number of parts to split the model into
    estimators = config["model"]["estimators"]
    model_dir = config["data"]["modeldir"]
    num_parts = estimators

    # Split the model into parts
    model_parts = []
    for i in range(num_parts):
        model_part = (
            f"{model_dir}/randomforestregressor_trained_nomax_{estimators}_{i}.joblib"
        )
        logging.info(f"dumping part {i}")
        joblib.dump(model.estimators_[i], model_part)
        model_parts.append(model_part)
    # persist extra components of model
    feature_exp = model.feature_names_in_
    n_features_exp = model.n_features_in_
    n_outputs_exp = model.n_outputs_
    estimator_exp = model.estimator_
    joblib.dump(n_features_exp, f"{model_dir}/n_features_exp_{estimators}.joblib")
    joblib.dump(n_outputs_exp, f"{model_dir}/outputs_exp_{estimators}.joblib")
    joblib.dump(estimator_exp, f"{model_dir}/estimator_exp_{estimators}.joblib")
    joblib.dump(feature_exp, f"{model_dir}/feature_exp_{estimators}.joblib")
    # Persist the list of model parts to disk
    joblib.dump(
        model_parts, f"{model_dir}/random_forest_model_parts_{estimators}.joblib"
    )


def getsplitmodel(config):
    model_dir = config["data"]["modeldir"]
    estimators = config["model"]["estimators"]
    random_state = config["model"]["random_state"]
    n_jobs = config["model"]["n_jobs"]
    # Load the list of model parts
    model_parts = joblib.load(
        f"{model_dir}/random_forest_model_parts_{estimators}.joblib"
    )
    n_features = joblib.load(f"{model_dir}/n_features_exp_{estimators}.joblib")
    n_outputs = joblib.load(f"{model_dir}/outputs_exp_{estimators}.joblib")
    estimator = joblib.load(f"{model_dir}/estimator_exp_{estimators}.joblib")
    feature_names = joblib.load(f"{model_dir}/feature_exp_{estimators}.joblib")

    # Reload the model from the parts
    lmodel = []
    for part_file in model_parts:
        logging.info(f"loading part {part_file}")
        part = joblib.load(part_file)
        lmodel.append(part)

    # Create the RandomForestRegressor model instance
    # Create a RandomForestRegressor model
    loaded_model = RandomForestRegressor(
        n_estimators=estimators, random_state=random_state, n_jobs=n_jobs, verbose=1
    )
    # loaded_model = RandomForestRegressor(n_estimators=len(lmodel))
    loaded_model.estimators_ = lmodel
    loaded_model.feature_names_in_ = feature_names
    loaded_model.n_features_in_ = n_features
    loaded_model.n_outputs_ = n_outputs
    loaded_model.estimator_ = estimator

    # Assign the feature names to the model
    return loaded_model


def getcleandata(config):
    featuredir = config["data"]["featuredir"]

    data = pd.read_parquet(featuredir)
    logging.info("read feature data")

    # Assume `data` is loaded as a Pandas DataFrame
    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)
    # Remove rows with NaN values
    data.dropna(inplace=True)
    logging.info("cleaned data")
    return data
