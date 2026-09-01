import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np 
import sqlite3
import pandas as pd 
import io
import base64

def main():

    correlation, image_base64 = get_graph("recession","unemployment benefits")
    print(correlation)
    print(len(image_base64))

  
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

    x_numeric = np.array(wide.index.map(lambda d: d.toordinal()))

    M = 3 # the polynomial curve 

    coeffs_a = np.polyfit(x_numeric, wide[term_a], M)# find the best fot curve(degree 3) that matches x-value(x_numeric) and then y-value(wide[term(a)])
    poly_a = np.polyval(coeffs_a, x_numeric) # now calculate the y-values at each pf this x-value points 

    # similar thing to be done for the second term 
    coeffs_b = np.polyfit(x_numeric, wide[term_b], M)
    poly_b = np.polyval(coeffs_b, x_numeric)

    #create the overall figure and one axis to start 
    fig, ax_left = plt.subplots(figsize=(12,6))#12 wide and 6 tall

    # plot your data point(dates on x, terms values on y and also customization 

    #first for the y-axis 
    ax_left.scatter(wide.index, wide[term_a], color = "tab:blue", s = 45, alpha = 0.8, edgecolor = "black", label = term_a) # in this specfic area draw individual dots 
    ax_left.plot(wide.index, poly_a, color = "blue", linewidth=2, label=f"Fit:{term_a.capitalize()}") #draw a connected line instead of just seperated dots, this is the polynomial fit curve
    ax_left.set_ylabel(term_a.capitalize(), color="tab:blue") # label the left axis and give it its color 
    ax_left.tick_params(axis="y", labelcolor = "tab:blue") # the color of the tick marks along the y axis 

    # then for the x-axis 
    ax_right = ax_left.twinx() # new axis that shares the x-axis with ax_left but has its own y-axis is what were doing 
    ax_right.scatter(wide.index, wide[term_b], color = "tab:red", s = 45, alpha = 0.8, edgecolor = "black", label = term_b)
    ax_right.plot(wide.index, poly_b, color = "red", linewidth = 2, label = f"Fit:{term_b.capitalize()}")
    ax_right.set_ylabel(term_b.capitalize(), color="tab:red")
    ax_right.tick_params(axis="y", labelcolor = "tab:red")

    # add a title for the graph 
    #plt.title(f"{term_a.capitalize()} vs {term_b.capitalize()}", weight = "bold")

    # add the legend to the graph
    # we need to use .get_legend_handles() so the two acis can know about each other 
        #.get_legend_handles() ask out of everything drawn get the visual obkecs and the text name
    lines1, labels1 = ax_left.get_legend_handles_labels()  #  labels is [term_a, f"Fit ({term_a})"]
    lines2, labels2 = ax_right.get_legend_handles_labels() 


    # then we creat the legned with both the lines and labes together 
    ax_left.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize = 10)

    # add the correlation label 
    # edit no need know since were also putting this on the graph through html 
    #fig.text(0.33, 0.03, f"Pearson Correlation coefficient: r = {correlation}") # places text anywhere based of the x & y cordinates 

    # layout adjustment/ nuge the plotting area so the bottome correlation text sits outside the plot area
    # edit(no need now since we decide to put it on the graph through html instead)
    fig.tight_layout()

    #display the graph 
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return correlation, image_base64

if __name__ == "__main__":
    main() 