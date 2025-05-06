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

    # Fetch historical data
    us_debt = yf.Ticker(debt_ticker)

    # Get the most recent closing value
    risk_free_rate = us_debt.fast_info.last_price
    risk_free_rate /= 100

    return risk_free_rate

def get_exchange_rate():
    cadusd = yf.Ticker('CADUSD=x')
    # Will edit these later
    start_date = '2023-11-14'
    end_date = '2025-03-01'

    cadusd_history = cadusd.history(start=start_date, end=end_date)['Close']
    cadusd_history.index = cadusd_history.index.strftime('%Y-%m-%d')

    return cadusd_history

def get_benchmark_index():
    TSX_index = yf.Ticker('^GSPTSE')
    SP_index = yf.Ticker('^GSPC')
    start_date = '2023-11-14'
    end_date = '2025-03-01'

    TSX_index_hist = TSX_index.history(start=start_date, end=end_date)['Close']
    TSX_index_hist.index = TSX_index_hist.index.strftime('%Y-%m-%d')
    SP_index_hist = SP_index.history(start=start_date, end=end_date)['Close']
    SP_index_hist.index = SP_index_hist.index.strftime('%Y-%m-%d')

    TSX_index_hist = TSX_index_hist * get_exchange_rate()

    indices = pd.DataFrame()
    indices['SP Index'] = SP_index_hist
    indices['TSX Index (USD)'] = TSX_index_hist
    return indices

def getBeta(cur_ticker):
    cur_stock = yf.Ticker(cur_ticker)

    # Will edit these later
    start_date = '2023-11-14'
    end_date = '2025-03-01'

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
    todays_price = cur_stock.fast_info.last_price

    if currency == 'CAD':
        exchange = yf.Ticker('CADUSD=x').fast_info.last_price
        todays_price = todays_price * exchange
    
    return SP_beta.iat[0,1], todays_price

# Gets average of daily growth
def getGrowth(cur_ticker):
    # Fetch data for current stock
    cur_stock = yf.Ticker(cur_ticker)
    start_date = '2023-11-14'
    end_date = '2025-03-01'
    cur_stock_hist = cur_stock.history(start=start_date, end=end_date)

    prices = pd.DataFrame()
    prices[cur_ticker] = cur_stock_hist['Close']
    
    daily_returns = prices.pct_change(fill_method=None).dropna()
    SP_growth = daily_returns.mean()
    
    return SP_growth[cur_ticker] * 100

def getVolatility(cur_ticker):
    start_date = '2023-11-14'
    end_date = '2025-03-01'
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

def get_best_port(best_portfolios, max_stocks, min_stocks):
    best_port = pd.DataFrame()
    best_investment_coeff = float('-inf')
    best_index = -1
    for i in range(min_stocks, max_stocks):
        cur_portfolio = best_portfolios[i]
        cur_investment_coeff = cur_portfolio['Investment Coefficient'].iloc[0]

        if cur_investment_coeff > best_investment_coeff:
            best_investment_coeff = cur_investment_coeff
            best_port = cur_portfolio
            best_index = i
    
    Portfolio_Final = pd.DataFrame()
    for i in range(len(best_port) - 1):
        new_row = {
            'Ticker': best_port["Name"].iloc[i],
            'Price': best_port["price"].iloc[i],
            'Currency': 'USD',
            'Shares': best_port["shares"].iloc[i],
            'Value': best_port["spent"].iloc[i] - best_port["transaction fees"].iloc[i],
            'Weight': best_port["weight"].iloc[i],
        }
        Portfolio_Final = pd.concat([Portfolio_Final, pd.DataFrame(new_row, index=[0])], ignore_index=True)

    Portfolio_Final.index = Portfolio_Final.index + 1

    return Portfolio_Final, best_index