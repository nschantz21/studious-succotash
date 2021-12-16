# imports
import argparse
from csv import DictReader, DictWriter
from collections import defaultdict

# constants
output_fields = [
    'timestamp', 'price', 'side',
    'bp0','bp1', 'bp2', 'bp3', 'bp4',
    'bq0', 'bq1', 'bq2', 'bq3', 'bq4',
    'ap0', 'ap1', 'ap2', 'ap3', 'ap4',
    'aq0', 'aq1', 'aq2', 'aq3', 'aq4',
]
topn = 5

# command line interface
parser = argparse.ArgumentParser(description="Generate Orderbook from orders")
parser.add_argument("input_file", type=str, help="orders file")
parser.add_argument("output_file", type=str, help="orderbook file destination")

args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file

# I decided to implement this with two sets of dicts
# one to track order ids
bid_dict = dict()
ask_dict = dict()

# one to track price indexed 
bid_price_dict = defaultdict(int)
ask_price_dict = defaultdict(int)

count = 0
with open(input_file, 'r') as read_obj, open(output_file, 'w') as write_obj:
    # set up csv files
    csv_reader = DictReader(read_obj)
    csv_writer = DictWriter(write_obj, fieldnames=output_fields)
    csv_writer.writeheader()

    for row in csv_reader:
        # bids
        if row["side"] == 'b':
            if row["action"] == 'a':
                bid_dict[row["id"]] = [row['price'], row['quantity']]
                bid_price_dict[int(row["price"])] += int(row["quantity"])
            elif row["action"] == 'd':
                del bid_dict[row["id"]]
                bid_price_dict[int(row["price"])] -= int(row["quantity"])
            else:
                # go look up what the previous version
                p, q = bid_dict[row["id"]]
                # update the price dict
                bid_price_dict[int(p)] -= int(q)
                # add the new order
                bid_price_dict[int(row["price"])] += int(row["quantity"])
                # update the id dict
                bid_dict[row["id"]] = [row['price'], row['quantity']]
        # asks
        else:
            if row["action"] == 'a':
                ask_dict[row["id"]] = [row['price'], row['quantity']]
                ask_price_dict[int(row["price"])] += int(row["quantity"])
            elif row["action"] == 'd':
                del ask_dict[row["id"]]
                ask_price_dict[int(row["price"])] -= int(row["quantity"])
            else:
                # go look up what the previous version
                p, q = ask_dict[row["id"]]
                # update the price dict
                ask_price_dict[int(p)] -= int(q)
                # add the new order
                ask_price_dict[int(row["price"])] += int(row["quantity"])
                # update the id dict
                ask_dict[row["id"]] = [row['price'], row['quantity']]
        
        sorted_bids = sorted(filter(lambda x: x[1] > 0, bid_price_dict.items()), reverse=True)
        sorted_asks = sorted(filter(lambda x: x[1] > 0, ask_price_dict.items()))

        best_bids = sorted_bids[:topn]
        #worst_bids = sorted_bids[-5:]
        best_asks = sorted_asks[:topn]
        #worst_asks = sorted_asks[-5:]

        # write to the output file
        output_dict = {
            "timestamp":row["timestamp"],
            "side":row["side"],
            "price":row["price"],
        }

        for x in range(topn):
            output_dict["bq{}".format(x)] = 0
            output_dict["aq{}".format(x)] = 0

        for x in range(len(best_bids)):
            output_dict["bp{}".format(x)] = best_bids[x][0]
            output_dict["bq{}".format(x)] = best_bids[x][1]

        for x in range(len(best_asks)):
            output_dict["ap{}".format(x)] = best_asks[x][0]
            output_dict["aq{}".format(x)] = best_asks[x][1]

        csv_writer.writerow(output_dict)
        if count % 10000 == 0:
            print(count)
        count+=1
