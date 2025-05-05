import pandas as pd
import numpy as np
import yfinance as yf
import random

def get_rf():
    """
    Fetches the most recent 3-month US government debt rate from Yahoo Finance.
    """
    # Defining the ticker for 3-month US government debt
    debt_ticker = '^IRX'
    start_date = '2024-11-22'
    end_date = '2024-11-23'

    # Fetch historical data
    us_debt = yf.Ticker(debt_ticker)

    # Print the most recent closing value
    risk_free_rate = us_debt.fast_info.last_price
    risk_free_rate /= 100

    return risk_free_rate

def get_exchange_rate():
    cadusd = yf.Ticker('CADUSD=x')
    # Will edit these later
    start_date = '2023-11-14'
    end_date = '2024-11-23'

    cadusd_history = cadusd.history(start=start_date, end=end_date)['Close']
    cadusd_history.index = cadusd_history.index.strftime('%Y-%m-%d')

    return cadusd_history

def get_benchmark_index():
    TSX_index = yf.Ticker('^GSPTSE')
    SP_index = yf.Ticker('^GSPC')
    start_date = '2023-11-14'
    end_date = '2024-11-23'

    TSX_index_hist = TSX_index.history(start=start_date, end=end_date)['Close']
    TSX_index_hist.index = TSX_index_hist.index.strftime('%Y-%m-%d')
    SP_index_hist = SP_index.history(start=start_date, end=end_date)['Close']
    SP_index_hist.index = SP_index_hist.index.strftime('%Y-%m-%d')

    TSX_index_hist = TSX_index_hist * get_exchange_rate()

    indices = pd.DataFrame()
    indices['SP Index'] = SP_index_hist
    indices['TSX Index'] = TSX_index_hist
    return indices

def getBeta(cur_ticker):
    cur_stock = yf.Ticker(cur_ticker)

    # Will edit these later
    start_date = '2023-11-14'
    end_date = '2024-11-23'

    cur_stock_hist = cur_stock.history(start=start_date, end=end_date)
    cur_stock_hist.index = cur_stock_hist.index.strftime('%Y-%m-%d')

    indices = get_benchmark_index()

    prices = pd.DataFrame()
    prices[cur_ticker] = pd.DataFrame(cur_stock_hist['Close'])
    prices['SP Index'] = indices['SP Index']

    daily_returns = prices.pct_change(fill_method=None).dropna()
    daily_returns.drop(index=daily_returns.index[0], inplace=True)

    SP_var = daily_returns['SP Index'].var()
    SP_beta = daily_returns.cov() / SP_var
    currency = cur_stock.fast_info.currency
    todays_price = prices[cur_ticker].iloc[-1]

    if currency == 'CAD':
        exchange = yf.Ticker('CADUSD=x').fast_info.last_price
        todays_price = todays_price * exchange
    
    return SP_beta.iat[0,1], todays_price

# Gets average of daily growth
def getGrowth(cur_ticker):
    # Fetch data for current stock
    cur_stock = yf.Ticker(cur_ticker)
    start_date = '2023-11-14'
    end_date = '2024-11-23'
    cur_stock_hist = cur_stock.history(start=start_date, end=end_date)

    prices = pd.DataFrame()
    prices[cur_ticker] = cur_stock_hist['Close']
    
    daily_returns = prices.pct_change(fill_method=None).dropna()
    SP_growth = daily_returns.mean()
    
    return SP_growth[cur_ticker] * 100

def getVolatility(cur_ticker):
    start_date = '2023-11-14'
    end_date = '2024-11-23'
    stock_data = yf.Ticker(cur_ticker).history(start=start_date, end=end_date)
    stock_data['Daily Return'] = stock_data['Close'].pct_change(fill_method=None).dropna()
    
    volatility = stock_data['Daily Return'].std()
    return volatility

def generate_numbers(n, min_value, max_value, total_sum):
    total_lower = n * min_value
    total_upper = n * max_value
    if total_sum < total_lower or total_sum > total_upper:
        raise ValueError("Cannot generate numbers with the given constraints.")

    # Calculate the adjusted sum we need to distribute
    remaining_sum = total_sum - total_lower
    adjusted_upper_bounds = [max_value - min_value] * n

    # Generate initial random values
    u = [random.random() for _ in range(n)]
    adjusted_weights = [u_i * adjusted_upper_bounds[i] for i, u_i in enumerate(u)]
    adjusted_weights_sum = np.sum(adjusted_weights)

    # Scale the weights to match the remaining sum
    scaling_factor = remaining_sum / adjusted_weights_sum
    adjusted_weights = [w_i * scaling_factor for w_i in adjusted_weights]

    # Compute the final values
    x = [min_value + w_i for w_i in adjusted_weights]

    return x

