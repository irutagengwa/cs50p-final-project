import sqlite3
from flask import Flask 

app = Flask(__name__)

# when someone visits the url path(/)(homepage) run the function below 
@app.route("/")
def home():
    # connect to the database & cursor for to excute commands 
    connect = sqlite3.connect("data/trends.db")
    cursor = connect.cursor()

    #excute the querey 
    cursor.execute("SELECT * FROM data")

    # collect the rows and the print them line by line 

    rows = cursor.fetchall()
    full_data = []

    for row in rows:
        full_data.append(row)
    return full_data
    
    #close the connections/(Always cursosr first)
    cursor.close()
    connect.close()




# debug=True for automatic reloader & Error Messages 
if __name__ == "__main__":
    app.run(debug=True)