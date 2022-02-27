import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import yfinance as yf
from tqdm.auto import tqdm
import re

load_dotenv()
tqdm.pandas()

# URL = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={os.environ['alphavantage_key']}"
# df = pd.read_csv(URL)
# df = df[df['estimate'] > 0]

# df.to_csv("data.csv")

df = pd.read_csv("data.csv")

df = df.sample(2000)

symbols = df['symbol'].tolist()
data = yf.download(symbols, period="1d")
data = data["Close"]

def get_unit_estimate(row):
    symbol = row["symbol"]
    estimate = row["estimate"]
    close = [x for x in data[symbol] if np.isnan(x) == False]
    if len(close) == 0:
        return pd.NA
    return (estimate / close[0])


df["unit_estimate"] = df.progress_apply(get_unit_estimate, axis=1)

df = df.sort_values("unit_estimate", ascending=False).head(10)


def get_beta(row):
    url = f'https://finance.yahoo.com/quote/{row["symbol"]}/key-statistics/'
    html = requests.get(url, headers={'User-Agent': 'Custom'}).text
    html = re.sub(r'\s|\n|\r', '', html)

    pattern = r"Beta\(5YMonthly\).*?<td.*?>(.*?)</td>"
    match = re.search(pattern, html)
    try:
        return float(match.group(1))
    except ValueError:
        return pd.NA


df["beta"] = df.progress_apply(get_beta, axis=1)

df["beta_rel"] = abs(1 - df["beta"])
df = df.sort_values("beta_rel")

df.to_csv("sorted.csv")

df.rename(columns={'symbol': 'Symbol', "name": "Name", "estimate": "Estimated earnings (3mo)", "currency": "Currency", "unit_estimate": "Relative earnings (3mo)", "beta": "Beta Value"}, inplace=True)
df.drop(columns=["reportDate", "fiscalDateEnding", "beta_rel"], inplace=True)
df.to_csv("templates/investment/api_data/stored.csv", index=False)