# kaggle datasets download -d jacksoncrow/stock-market-dataset
# assumes kaggle.json configured correctly
import kaggle

kaggle.api.authenticate()

kaggle.api.dataset_download_files('jacksoncrow/stock-market-dataset', path='/data/kaggle', unzip=True)


