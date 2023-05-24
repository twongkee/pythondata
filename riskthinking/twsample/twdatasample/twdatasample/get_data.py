# kaggle datasets download -d jacksoncrow/stock-market-dataset
# assumes kaggle.json configured correctly
import kaggle
from twdatasample.twutils import getconfig

config = {}
config = getconfig()

kaggle.api.authenticate()

datapath = config["data"]["kaggle"]
kaggle.api.dataset_download_files(
    "jacksoncrow/stock-market-dataset", path=datapath, unzip=True
)
