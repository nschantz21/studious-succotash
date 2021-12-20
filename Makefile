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
	echo "Making Features"
	python -m src.features.build_features 20190610
	python -m src.features.build_features 20190611
	python -m src.features.build_features 20190612
	python -m src.features.build_features 20190613
	python -m src.features.build_features 20190614

train_models:
	echo "Making the Model"
	python -m src.models.train_model 20190610
	python -m src.models.train_model 20190611
	python -m src.models.train_model 20190612
	python -m src.models.train_model 20190613
	python -m src.models.train_model 20190614

predict_models:
	for date in 10 11 12 13 14 ; do \
		python -m src.models.predict_model 201906$$date 201906$$date ; \
	done
