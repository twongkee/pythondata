echo "shrink data set for fast tests"
echo "delete all but IBM stock ad etfs"

cd /twdata/kaggle
mkdir full
mv etfs/ stocks/ full
mkdir etfs
mkdir stocks
cp full/stocks/IBM.csv stocks/
cp full/etfs/IBM* etfs/
echo "shrunk" >> /twdata/shrunk.log
