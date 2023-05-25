# kaggle datasets download -d jacksoncrow/stock-market-dataset
# assumes kaggle.json configured correctly
import kaggle
from twdatasample.twutils import getconfig, setuplogging

config = {}
config = getconfig()

mylogger = setuplogging(config)

mylogger.info(
    "============================================================================="
)
mylogger.info("started get data")

kaggle.api.authenticate()

datapath = config["data"]["kaggle"]
datasource = config["data"]["source"]
mylogger.info(f"getting from {datasource}")
kaggle.api.dataset_download_files(f"{datasource}", path=datapath, unzip=True)
mylogger.info("completed get data")
