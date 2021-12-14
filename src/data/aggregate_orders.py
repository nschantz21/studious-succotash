# imports
import pandas as pd
import numpy as np

# constants
output_fields = [
    'timestamp',
    'price',
    'side',
    'bp0','bp1', 'bp2', 'bp3', 'bp4',
    'bq0', 'bq1', 'bq2', 'bq3', 'bq4',
    'ap0', 'ap1', 'ap2', 'ap3', 'ap4',
    'aq0', 'aq1', 'aq2', 'aq3', 'aq4',
]

# add arg parse here
input_fp = "data/external/res_20190610.csv"
orders = pd.read_csv(input_fp)

# create empty orderbook
orderbook = pd.DataFrame(columns=output_fields)

# iterate through the orders
for index, row in orders.iterrows():
    pass

