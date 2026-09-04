# TrendSignal
#### [Video Demo](http://youtube.com/watch?v=GlXUyHiE4QA)
## Description

TrendSignal is a web application I built to explore whether public search interest, via [Google Trends](https://trends.google.com/trends/), can act as an early signal for real-world events. Users pick two search terms, and the site calculates and visualizes the statistical correlation between them over time.

The idea is built on the observation that search behavior often shifts before an event shows up in official statistics: people search "unemployment benefits" before jobless claims are reported, or "flu symptoms" before case counts rise. Public interest often moves first, and official numbers catch up weeks later. TrendSignal lets a user pick two terms and see, numerically and visually, how closely they actually move together, rather than just taking that intuition on faith.

This project grew out of research I did in high school looking at Google Trends data as a proxy signal alongside COVID-19 case counts, and out of a broader interest in how accessible, publicly available data (search interest, in this case) can stand in for information that's otherwise slow, expensive, or hard to collect, particularly in contexts where official reporting lags or is unreliable. TrendSignal is a smaller, self-contained version of that same question: can something as simple as search volume tell you something true about the world, and how would you actually check?

## How it works

TrendSignal is organized around a simple pipeline: **Collect → Store → Compare → Visualize**. Each step has one job, and each only talks to the step next to it.

1. **Collect.** A one-time Python script (`fetch_data.py`) uses the `pytrends` an unofficial API to collect Google Trends data, it pulls 5 years of weekly search interest data from Google Trends for each term in a curated list, spanning categories like health, economy, and seasonal topics. This runs independently of the live website, so the site itself never depends on Google being reachable at the moment someone visits.

2. **Store.** That data is saved into a local SQLite database, with each row recording a single term, date, and interest value (0 to 100, Google's own normalized scale). Because the data is pre-fetched rather than pulled live, the site responds instantly and isn't vulnerable to rate limits, API changes, or outages on Google's end.

3. **Compare.** When a visitor selects two terms and submits the form, a Flask route queries the database for just those two terms, aligns their values by date using pandas, and computes the Pearson correlation coefficient between them, a single number from -1 to 1 describing how closely the two move together, and in which direction.

4. **Visualize.** The same two terms are plotted on a dual-axis scatter chart, each with its own best-fit polynomial curve, using Matplotlib. Each term gets its own y-axis, since two search terms can have very different overall popularity, and a dual axis keeps a lower-volume term readable instead of flattening it near zero. The chart is rendered entirely in memory and embedded directly into the page, with no image files ever written to disk.

Everything downstream of "collect" (comparing terms, drawing charts, serving pages) runs entirely off the local database, which is what makes the whole thing fast, resilient to Google's own scraping restrictions, and simple to extend with new terms later.

## How to use 

Run project.py in your teminal, select the two terms you would like to compare, then press compare !!

Special thanks to my friends for working on the html and css code.
