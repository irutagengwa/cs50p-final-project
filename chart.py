import sqlite3
import pandas as pd 

connect = sqlite3.connect("data/trends.db")
df = pd.read_sql_query("SELECT * FROM data", connect)
connect.close()

wide = df.pivot(index="date", columns="term", values="value")

correlation = wide["unemployment benefits"].corr(wide["recession"])

print(correlation)
