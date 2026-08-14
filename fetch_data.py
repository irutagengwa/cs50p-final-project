import sqlite3
from pytrends.request import TrendReq

# we are going to connect the sqlite datbase to the file we want to connect
connect = sqlite3.connect("data/trends.db")

# connect to Google with an object
pytrends = TrendReq(hl="en-US", tz=360, timeout=(20, 25))


# Build payload/ the core data transmitted
kw_list = ["unemployment benefits", "flu symptoms", "recession", "pumpkin spice"]

pytrends.build_payload(kw_list, timeframe="today 5-y", geo="US")


# print the pytrends intrest overtime and see what we get

data = pytrends.interest_over_time()

print(data.head())


