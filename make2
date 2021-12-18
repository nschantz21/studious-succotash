# Bash file for easy data creation
unzip data/external/3rqtest.zip -x *.docx -d data/raw/

python -m src.data.make_orderbook \
data/raw/codetest/res_20190610.csv \
data/interim/20190610.csv

python -m src.data.make_orderbook \
data/raw/codetest/res_20190611.csv \
data/interim/20190611.csv

python -m src.data.make_orderbook \
data/raw/codetest/res_20190612.csv \
data/interim/20190612.csv

python -m src.data.make_orderbook \
data/raw/codetest/res_20190613.csv \
data/interim/20190613.csv

python -m src.data.make_orderbook \
data/raw/codetest/res_20190614.csv \
data/interim/20190614.csv
