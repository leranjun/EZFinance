import CALCULATOR as calc
import sys
import yfinance as yf
import json

class compare:
    def __init__(self):
        pass
    def compare(self):
        symbol = sys.argv[1]

        shortterm = calc.ShortTerm()

        shortterm.short_term(input)

        data = yf.download(tickers=input, period='5d', interval='5m')
        close = data['Close']
        close2 = close.iloc[-2]

        x = {}
        with open("range.json","r") as f:
            x = json.load(f)

        if close2 < x[input+"_lower"]:
            return("sell")
        elif close2 > x[input+"_higher"]:
            return("buy")