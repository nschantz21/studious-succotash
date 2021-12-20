# imports
import pandas as pd
import random
import argparse



# constants

p = 0.1  # percent of lines in file to sample
random.seed(42)
liquidity_steps_forward = 5000

# arg parser
parser = argparse.ArgumentParser()
parser.add_argument("input_file_name", type=str)
args = parser.parse_args()

input_file_name = args.input_file_name
input_data_fp = "data/interim/{}.csv".format(input_file_name)
# import sample of data
df = pd.read_csv(
         input_data_fp,
         header=0, 
         skiprows=lambda i: i>0 and random.random() > p)

df.drop_duplicates(subset="timestamp", inplace=True)

# calculate the bid-ask spreads and balance of quantities at each level
for x in range(5):
    df["spread{}".format(x)] = df["ap{}".format(x)] - df["bp{}".format(x)]
    # spread balance: positive is excess demand, negative is excess supply
    df["spread_balance_{}".format(x)] = df["bq{}".format(x)] - df["aq{}".format(x)]

momentum = df["price"].diff(liquidity_steps_forward).rename("momentum")
balances = df.filter(regex="spread_balance_0").diff(liquidity_steps_forward).shift(-liquidity_steps_forward).iloc[:,0].rename("fwd_liq")

other_balances = df.filter(regex="spread_balance_[0-4]").diff(liquidity_steps_forward)

# volatility
price_volatility = df["price"].rolling(liquidity_steps_forward).std().rename("price_volatility")


liquidity_features = pd.concat(
    [
        balances,
        other_balances,
        momentum,
        price_volatility,
        df["bid_vwap"].diff(liquidity_steps_forward), df["ask_vwap"].diff(liquidity_steps_forward)
     ],
     axis=1).dropna()

liquidity_features.to_csv("data/processed/{}.csv".format(input_file_name))
