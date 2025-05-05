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
