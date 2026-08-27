import matplotlib
matplotlib.use("Agg") # sets Matplotlib backend to a non-interactive, non-GUI rendering engine will render in memory/hence no pop-up
import matplotlib.pyplot as plt
import numpy as np 
import sqlite3
import pandas as pd 

def main():

   get_graph()

def get_graph(term_a, term_b):
    with sqlite3.connect("data/trends.db") as connect:
        df = pd.read_sql_query(
            "SELECT * FROM data WHERE term IN (?, ?)",
            connect,
            params=(term_a, term_b),
        )
    df["date"] = pd.to_datetime(df["date"])
    wide = df.pivot(index="date", columns="term", values="value")
    correlation = wide[term_a].corr(wide[term_b])

    x_numeric = np.array(df.index.map(lambda d: d.toordinal()))

    M = 3 # the polynomial curve 

    coeffs_a = np.polyfit(x_numeric, wide[term_a], M)# find the best fot curve(degree 3) that matches x-value(x_numeric) and then y-value(wide[term(a)])
    poly_a = np.polyval(coeffs_a, x_numeric) # now calculate the y-values at each pf this x-value points 

    # similar thing to be done for the secon term 
    coeffs_b = np.polyfit(x_numeric, wide[term_a], M)
    poly_b = np.polyval(coeffs_b, x_numeric)

    #create the overall figure and one axis to start 
    fig, ax_left = plt.subplot(figsize=(12,6))#12 wide and 6 tall

    # plot your data point(dates on x, terms values on y) and also customization 

    #first for the y-axis 
    ax_left.scatter(wide.index, wide[term_a], color = "tab:blue", s = 45, alpha = 0.8, edgecolor = "black", label = term_a) # in this specfic area draw individual dots 
    ax_left.plot(wide.index, poly_a, color = "blue", linewidth=2, label=f"Fit:({term_a})") #draw a connected line instead of just seperated dots, this is the polynomial fit curve
    ax_left.set_ylabel(term_a, color="tab:blue") # label the left axis and give it its color 
    ax_left.tick_params(axis="y", labelcolor = "tab:blue") # the color of the tick marks along the y axis 

    # then for the x-axis 
    ax_right = ax_left.twin() # this creates another axis but the key is this make sit that is shared with the first axis 
    ax_right.scatter(wide.index, wide[term_a], color = "tab:red", s = 45, alpha = 0.8, edgecolor = "black", label = term_b)
    ax_right.plot(wide.index, poly_b, color = "red", linewidet = 2, label = f"Fit:({term_b})")
    ax_right.set_xlabel(term_b, color="tab:red")
    ax_right.teck_params(axis="x", labelcolor = "tab:red")

    # add a title for the graph 
    plt.title(f"{term_a} vs {term_b}")

    # add the legend to the graph 
    lines1, labels1 = ax_left.get_legend_handles_labels()
    lines2, labels2 = ax_right.get_legend_handles_labels()
    ax_left.legnet(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize = 10)

    # add the correlation label 
    fig.text(0.5, 0.02, f"Pearson Correlation coefficientL r = {correlation}") # places text anywhere based of the x & y cordinates 

    # layout adjustment/ nuge the plotting area so the bottome correlation text sits outside the plot area
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])




if __name__ == "__main__":
    main() 