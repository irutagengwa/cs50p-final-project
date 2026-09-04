import sqlite3
from flask import Flask, render_template, request
from chart import get_graph, DB_PATH
import os 

app = Flask(__name__)


def get_available_terms():
    with sqlite3.connect(DB_PATH) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT DISTINCT term FROM data ORDER BY term")
        terms = [row[0] for row in cursor.fetchall()]
    return terms


def validate_terms(term_a, term_b, terms):
    """Return an error message for a bad pair of terms, or None if the pair is fine."""
    # somebody could hit /compare by hand with a missing or made up term, so check first
    if term_a not in terms or term_b not in terms:
        return "Please pick two terms from the list."
    if term_a == term_b:
        return "Please pick two different terms."
    return None


def describe_correlation(correlation):
    """Turn an r value into the wording the page shows next to the number."""
    mag = abs(correlation)
    if mag > 0.8:
        strength = "Very strong"
    elif mag > 0.6:
        strength = "Strong"
    elif mag > 0.4:
        strength = "Moderate"
    elif mag > 0.2:
        strength = "Weak"
    else:
        strength = "Essentially no"
    direction = "negative" if correlation < 0 else "positive"
    return f"{strength} {direction} relationship"


# so this is going to be our homepage and we want there just to be the form, no chart yet
@app.route("/")
def home():
    terms = get_available_terms()
    return render_template("index.html", terms=terms)


# ok now when someone writes something on the form, this route reads their picks and builds the chart
@app.route("/compare")
def compare():
    term_a = request.args.get("term_a")
    term_b = request.args.get("term_b")

    # the form is always rebuilt, so the dropdowns still have options after comparing
    terms = get_available_terms()

    error = validate_terms(term_a, term_b, terms)
    if error:
        return render_template(
            "index.html",
            terms=terms,
            error=error,
            term_a=term_a,
            term_b=term_b,
        ), 400

    correlation, image = get_graph(term_a, term_b)

    return render_template(
        "index.html",
        terms=terms,
        correlation=correlation,
        image=image,
        term_a=term_a,
        term_b=term_b,
    )


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
