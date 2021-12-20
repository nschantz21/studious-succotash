unzip: 
	unzip data/external/3rqtest.zip -x *.docx -d data/raw/

orderbooks: 
	python -m src.data.make_orderbook \
    data/raw/codetest/res_20190610.csv \
    data/interim/20190610.csv;

	python -m src.data.make_orderbook \
    data/raw/codetest/res_20190611.csv \
    data/interim/20190611.csv;
	
	python -m src.data.make_orderbook \
    data/raw/codetest/res_20190612.csv \
    data/interim/20190612.csv
	
	python -m src.data.make_orderbook \
    data/raw/codetest/res_20190613.csv \
    data/interim/20190613.csv
	
	python -m src.data.make_orderbook \
    data/raw/codetest/res_20190614.csv \
    data/interim/20190614.csv
    
features:
    #echo "Making Features"
	python -m src.features.build_features
    # I would make this more generalized with more time

#model:
    #echo "Making the Model"
