"""
Script to train and save models in this analysis
"""
# imports
import pandas as pd
from sklearn.linear_model import Lasso
import pickle  # to persist model
import argparse

# arg parser
parser = argparse.ArgumentParser()
parser.add_argument("input_file_name", type=str)
args = parser.parse_args()

input_file_name = args.input_file_name

# import data
df = pd.read_csv(
	"data/processed/{}.csv".format(input_file_name),
	index_col=0)
print(df.head())

# create regression model
reg = Lasso(alpha=1.0, max_iter=10000)
y = df.iloc[:, 0].values
X = df.iloc[:, 1:].values
print(len(X))
reg.fit(X,y)

# persist the model as a pickle binary object
with open('models/lasso_{}.pkl'.format(input_file_name),'wb') as f:
    pickle.dump(reg,f)
