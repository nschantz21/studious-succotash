# imports
import pandas as pd
import argparse

# constants
output_fields = [
    'timestamp', 'price', 'side',
    'bp0','bp1', 'bp2', 'bp3', 'bp4',
    'bq0', 'bq1', 'bq2', 'bq3', 'bq4',
    'ap0', 'ap1', 'ap2', 'ap3', 'ap4',
    'aq0', 'aq1', 'aq2', 'aq3', 'aq4',
]

# command line interface
parser = argparse.ArgumentParser(description="Generate Orderbook from orders")
parser.add_argument("input_file", type=str, help="orders file")
parser.add_argument("output_file", type=str, help="orderbook file destination")

args = parser.parse_args()
input_fp = args.input_file


# create empty orderbook
orderbook = pd.DataFrame(columns=output_fields)

helper_fields = ["id", "price", "quantity"]

buy_frame = pd.DataFrame(columns=helper_fields).set_index("id")
sell_frame = pd.DataFrame(columns=helper_fields).set_index("id")

chunksize=10**4
for chunk in pd.read_csv(input_fp, chunksize=chunksize):
    # iterate through the orders
    for index, row in chunk.iterrows():
        side = row["side"]
        action = row["action"]
        r = row.to_frame().T[helper_fields].set_index("id")
    
        if side == 'b':
            if action == "a":
                buy_frame = buy_frame.append(r)
            elif action == "d":
                buy_frame.drop(labels=r.index, inplace=True)
            else:
                # modified orders
                buy_frame.update(r)
        else:
            if action == "a":
                sell_frame = sell_frame.append(r)
            elif action == "d":
                sell_frame.drop(labels=r.index, inplace=True)
            else:
                # modified orders
                sell_frame.update(r)
        
        # calculate top buys
        bids = (
            buy_frame
            .groupby("price")["quantity"]
            .sum()
            .sort_index(ascending=False)
            .head(5)
        ).reset_index()
    
        # calculate top sells
        asks = (
            sell_frame
            .groupby("price")["quantity"]
            .sum()
            .sort_index(ascending=True)
            .head(5)
        ).reset_index()
    
        # generate new record to be added to orderbook
        output_dict = {
            "timestamp": row["timestamp"],
            "price": row["price"],
            "side": row["side"],
        }
        
        if ~bids.empty:
            output_dict.update(dict(zip(output_fields[3:8], bids["price"])))
            output_dict.update(dict(zip(output_fields[8:13], bids["quantity"])))
        if ~asks.empty:
            output_dict.update(dict(zip(output_fields[13:18], asks["price"])))
            output_dict.update(dict(zip(output_fields[18:], asks["quantity"])))
    
        orderbook = orderbook.append(
            pd.Series(output_dict),
            ignore_index=True)
    print(index)


# fill in zero quantities
quant_fields = list(orderbook.filter(regex="q"))
orderbook.fillna(
    dict(zip(quant_fields,[0.0 for qf in quant_fields])),
    inplace=True)
orderbook.to_csv(args.output_file)
