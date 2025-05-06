import pandas as pd
import numpy as np
import yfinance as yf
# import matplotlib.pyplot as plt
import random

print("hello")
ticker = yf.Ticker('MSFT')

# Will edit these later
start_date = '2023-11-14'
end_date = '2024-11-23'

name = ticker.info['shortName']

history = ticker.history(start=start_date, end=end_date)['Close']
history.index = history.index.strftime('%Y-%m-%d')

print(name)
print(history)

def get_name(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get('longName', "Unknown")

fixed_tickers = ['AAPL', 'MFC', 'SHOP', 'RY', 'NKE', 'MSFT', 'PG', 'NVDA', 'F', 'PFE', 'Afg', 'GOLD', 'BMO', 'SQ', 'TD', 'RCI', 'T', 'JPM', 'ENB', 'YO', 'BA', 'LLY', 'META', 'SPOT']
fixed_names = []
for ticker in fixed_tickers:
    name = get_name(ticker)
    print(name)
    fixed_names.append(name)

print(fixed_names)
print(len(fixed_names))
print(len(fixed_tickers))
