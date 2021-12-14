"""aggregate_orders.py

Aggregate Orders

This script corresponds to part 1 of the assessment.  
Write a program which reads an input csv, builds/updates the agg order book
for each order update, and outputs a new csv.

The output csv should contain one row per input row and, at a minimum, have
the timestamp of each update, the price and total quantity of the best 5
levels with non-zero quantity on each side of the book, and the price and side
of the update.

I over-commented for clarity and demonstration.
"""
# imports
import pandas as pd
from glob import iglob

# constants
external_data_path = "data/external/*.csv"

# data imports
orderbook_list = []
for raw_orders_file_path in iglob(external_data_path):
    # convert the file name into a date to add as a field
    file_date = pd.to_datetime(raw_orders_file_path[-12:-4])
    # read the data from the csv
    orders = pd.read_csv(raw_orders_file_path)
    # add the date as a field
    orders["date"] = file_date
    # add to collection of files for aggregation
    orderbook_list.append(orders)

orders_frame = pd.concat(orderbook_list)


# add the timestamp and date together for dattetime
orders_frame["datetime"] = (
    orders_frame["date"] +
    pd.to_timedelta(9.5, unit="h") +
    pd.to_timedelta(orders_frame["timestamp"], unit="us"))
print(orders_frame.sort_values("datetime"))