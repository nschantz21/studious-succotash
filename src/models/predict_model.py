import pickle
import pandas as pd
import argparse

# constants
parser = argparse.ArgumentParser()
parser.add_argument("model_name", type=str)
parser.add_argument("input_name", type=str)
args = parser.parse_args()

filename = args.model_name
filename2 = args.input_name

# data import
df = pd.read_csv(
	"data/processed/{}.csv".format(filename2),
	index_col=0)

# load the trained model
with open("models/lasso_{}.pkl".format(filename), "rb") as f:
	reg = pickle.load(f)

preds = reg.predict(df.iloc[:,1:].values)
df["preds"] = preds

# model-input
df.to_csv("data/predictions/{}-{}.csv".format(filename, filename2))
