import sqlite3
from flask import Flask, render_template, request
from chart import get_graph 

app = Flask(__name__)


def get_available_terms():
    with sqlite3.connect("data/trends.db") as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT DISTINCT term FROM data")
        terms = [row[0] for row in cursor.fetchall()]
    return terms 

# so this is going to be our homepage and we want there just to be the form, no chart yet 
@app.route("/")
def home():
   terms = get_available_terms()
   return render_template("index.html", terms = terms)


#ok now when somone writes something on the form, this route reas their picks and builds the chart 
@app.route("/compare")
def compare():
    term_a = request.args.get("term_a")
    term_b = request.args.get("term_b")

    correlation, image = get_graph(term_a, term_b)
    terms = get_available_terms()


    return render_template(
        "index.html",
        correlation = correlation,
        image = image,
        term_a = term_a,
        term_b = term_b
    )




if __name__ == "__main__":
    app.run(debug=True)