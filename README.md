# TrendSignal
#### [Video Demo](http://youtube.com/watch?v=GlXUyHiE4QA)
## Description

TrendSignal is a web application I built to explore whether public search interest, via [Google Trends](https://trends.google.com/trends/), can act as an early signal for real-world events. Users pick two search terms, and the site calculates and visualizes the statistical correlation between them over time.

The idea is built on the observation that search behavior often shifts before an event shows up in official statistics — people search "unemployment benefits" before jobless claims are reported, or "flu symptoms" before case counts rise. TrendSignal lets a user pick two terms and see, numerically and visually, how closely they actually move together.

## How it works

1. **Collect** — a one-time script pulls 5 years of weekly search interest for each term from Google Trends and saves it locally.
2. **Store** — that data lives in a small SQLite database, so the live site never has to call Google directly.
3. **Compare** — pick two terms on the site, and Flask pulls both from the database, aligns them by date, and computes their Pearson correlation coefficient.
4. **Visualize** — the two terms are plotted on a dual-axis chart with a best-fit curve each, so you can see not just the correlation number but the actual shape of how they move together.

## How to use 

Run project.py in your teminal, select the two terms you would like to compare, then press compare !!