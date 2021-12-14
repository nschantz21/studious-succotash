# imports
import pandas as pd
import numpy as np
from collections import defaultdict

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

helper_fields = ["timestamp", "side", "id", "quantity"]
buy_frame = pd.DataFrame(columns=helper_fields).set_index(helper_fields[:-1])
sell_frame = pd.DataFrame(columns=helper_fields).set_index(helper_fields[:-1])

# iterate through the orders
for index, row in orders.iterrows():
    side = row["side"]
    action = row["action"]
    print(row)

    rw = row.to_frame().set_index(helper_fields[:-1])
    if side == 'b':
        ob_helper = buy_frame
    else:
        ob_helper = sell_frame
    
    if action == "b":
        ob_helper.loc[rw.index] += rw["quantity"]
    if action == "d":
        ob_helper[hash("".join(row[["timestamp", "side", "id"]].values))] -= row["quantity"]
    else:
        ob_helper[hash(row[["timestamp", "side", "id"]].values)] = row["quantity"]
    
    print(ob_helper)
