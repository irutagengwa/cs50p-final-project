import sqlite3
from pytrends.request import TrendReq  # type: ignore
import sys

# we are going to connect the sqlite datbase to the file we want to connect
connect = sqlite3.connect("data/trends.db")

# adding a cursor()/ whats neceesary to excute sql statments
cursor = connect.cursor()

# create a column witht eh table values we want
cursor.execute("CREATE TABLE IF NOT EXISTS data(date, term, value, PRIMARY KEY (date, term))")

# we are first going to make sure the table was created

# connect to Google with an object
pytrends = TrendReq(hl="en-US", tz=360, timeout=(20, 25))


# Build payload/ the core data transmitted
kw_list = ["unemployment benefits", "flu symptoms", "recession", "pumpkin spice"]

pytrends.build_payload(kw_list, timeframe="today 5-y", geo="US")

# check if the table has actually been created and if not exit out of the program

res = cursor.execute("SELECT name FROM sqlite_master WHERE name = 'data'")
result = res.fetchone()

if result is None or result[0] != "data":
    sys.exit("Table was not created")


# print the pytrends intrest overtime and see what we get

data = pytrends.interest_over_time()

# No we are going to put the values we recive from pytrends to the table

for date, row in data.iterrows():

    # to get the data we put the
    for term in kw_list:
        value = row[term]

        cursor.execute(
            "INSERT INTO data (date, term, value) VALUES (?, ?, ?)",
            (str(date), term, int(value)),
        )

# Save the pending chnages to the file(commit) and shut the connection(.close)
connect.commit()
connect.close()
