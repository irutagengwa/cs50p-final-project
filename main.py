import sqlite3
from flask import Flask, render_template, request
from chart import get_graph, DB_PATH

app = Flask(__name__)


def get_available_terms():
    with sqlite3.connect(DB_PATH) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT DISTINCT term FROM data ORDER BY term")
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

    # the form is always rebuilt, so the dropdowns still have options after comparing
    terms = get_available_terms()

    # somebody could hit /compare by hand with a missing or made up term, so check first
    if term_a not in terms or term_b not in terms:
        return render_template(
            "index.html",
            terms = terms,
            error = "Please pick two terms from the list.",
            term_a = term_a,
            term_b = term_b
        ), 400

    correlation, image = get_graph(term_a, term_b)

    return render_template(
        "index.html",
        terms = terms,
        correlation = correlation,
        image = image,
        term_a = term_a,
        term_b = term_b
    )




if __name__ == "__main__":
    app.run(debug=True)
