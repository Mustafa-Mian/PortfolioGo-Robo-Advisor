import pandas as pd
import numpy as np
import yfinance as yf
import helpers as hp
import streamlit as st

def clean_data(tickers):
    tickers.drop_duplicates(inplace=True)
    
    if 0 in tickers.columns:
        tickers = tickers.rename(columns={0: 'name'})
    if 'name' not in tickers.columns:
        raise ValueError("Expected a 'name' column in the tickers DataFrame.")
        
    tickers['base_name'] = tickers['name'].str.replace(r'\.TO$', '', regex=True)
    tickers = tickers.drop_duplicates(subset='base_name')
    tickers = tickers.drop(columns=['base_name'])

    filtered_stocks = pd.DataFrame()
    start_date = "2023-10-01"
    end_date = '2025-03-01'
    for ticker in tickers['name']:
        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            if info['currency'] not in ["USD", "CAD"]: # Enusring stock is listed, traded in CAD or USD
                continue
    
            hist = stock.history(start=start_date, end=end_date, interval="1d")
            hist['Month'] = hist.index.to_period('M')
            monthly_data = hist.groupby('Month').filter(lambda x: len(x) >= 18)

            avg_monthly_volume = monthly_data.groupby('Month')['Volume'].mean().mean()
            if avg_monthly_volume >= 100000:
                filtered_stocks = pd.concat([filtered_stocks, pd.DataFrame({"Ticker": [ticker]})])
                
        except Exception as e:
            continue
    
    return filtered_stocks.reset_index(drop=True)


def rank(ticker_file):
    # Initialize the lists
    stock_data = []
    beta_data = []
    volatility_data = []
    growth_data = []

    # Iterate through the tickers and gather data
    for i in range(len(ticker_file)):
        cur_ticker = ticker_file['Ticker'].iloc[i]
        cur_stock = yf.Ticker(cur_ticker)
        start_date = '2023-11-14'
        end_date = '2025-03-01'
        cur_stock_hist = cur_stock.history(start=start_date, end=end_date)['Close']

        # Getting important statistics per stock
        beta, price = hp.getBeta(cur_ticker)
        beta_data.append({"name": cur_ticker, "beta": beta})
        growth = hp.getGrowth(cur_ticker)
        growth_data.append({"name": cur_ticker, "growth": growth})
        volatility = hp.getVolatility(cur_ticker)
        volatility_data.append({"name": cur_ticker, "volatility": volatility})

        # Store combined stock details
        stock_details = {
            "name": cur_ticker,
            "beta": beta,
            "growth": growth,
            "volatility": volatility,
            "price": price,
            "price_history": cur_stock_hist
        }
        stock_data.append(stock_details)

    # Sort the data by each criterion
    sorted_betas = sorted(beta_data, key=lambda d: d['beta'], reverse=True)
    sorted_growth = sorted(growth_data, key=lambda d: d['growth'], reverse=True)
    sorted_volatility = sorted(volatility_data, key=lambda d: d['volatility'], reverse=True)

    # Combine the lists into one iterable
    lists = [sorted_betas, sorted_growth, sorted_volatility]
    weights = [0.4, 0.3, 0.3]  # Corresponding weights for beta, growth, and volatility

    # Step 1: Calculate weighted average index position for each stock
    index_map = {}
    for weight, lst in zip(weights, lists):
        for index, stock in enumerate(lst):
            name = stock["name"]
            if name not in index_map:
                index_map[name] = 0
            # Add the weighted index to the total
            index_map[name] += index * weight

    # Step 2: Convert index_map to a list of dictionaries for sorting
    weighted_positions = [
        {"name": name, "weighted_index": total_index}
        for name, total_index in index_map.items()
    ]

    # Step 3: Sort stocks by their weighted index
    sorted_by_weighted = sorted(weighted_positions, key=lambda x: x["weighted_index"])

    # Final result: A list of stocks sorted by the weighted average of their index positions
    result = [{"name": stock["name"], "weighted_index": stock["weighted_index"]} for stock in sorted_by_weighted]

    return result, stock_data


""""""
def make_portfolios(stock_details, budget, flat_fee, fee_per_share, min_stocks, max_stocks):
    # Dictionary of best portfolio with 10, 11, ... n stocks
    strongest_portfolios = {}

    # Dictionary containing the daily value of the strongest_portfolios, backtested on a year's worth of data.
    back_testing_portfolios = {}

    risk_free_rate = hp.get_rf()

    for n in range(min_stocks, max_stocks):  # Loop through the number of stocks in the portfolio
        best_portfolio = None # DataFrame of best portfolio n stocks
        best_portfolio_backtesting = None
        best_invest_coeff = float('-inf') # Setting this value to an infinitely small number to begin

        for j in range(500):  # Create 500 portfolios with different weights for the current number of stocks
            stocks = stock_details[:n]
            max_weight = 15
            min_weight = 100 / (2 * n)
            generate = True
            
            # Generate valid weights for the portfolio
            while generate:
                weights = hp.generate_numbers(n, min_weight, max_weight, 100)
                if all(min_weight <= weight <= max_weight for weight in weights):
                    generate = False
            
            weights.sort(reverse=True)

            current_portfolio = pd.DataFrame()
            fees_spent = 0
            total_spent = 0

            # Create a dataframe for daily portfolio value calculation
            portfolio_values = pd.DataFrame()
            
            for i in range(len(stocks)):
                stock_weight = weights[i]
                money_allocated = budget * (stock_weight / 100)  # Allocate money based on weight
                
                # Deduct the flat fee initially to estimate spendable money
                money_for_stock = money_allocated - flat_fee
                
                if money_for_stock < 0:
                    shares = 0
                    transaction_fees = 0
                else:
                    shares = money_for_stock / stocks[i]["price"]  # Calculate shares
                    variable_fee = shares * fee_per_share
                    transaction_fees = min(flat_fee, variable_fee)  # Use the smaller fee
                    
                    # Adjust the number of shares based on fees
                    money_for_shares = money_allocated - transaction_fees
                    shares = money_for_shares / stocks[i]["price"]
                    actual_spent = shares * stocks[i]["price"] + transaction_fees
                    
                    # Update total spent and fees
                    total_spent += actual_spent
                    fees_spent += transaction_fees
                
                # Append stock details to the current portfolio
                new_row = {
                    'Name': stocks[i]["name"],
                    'weight': weights[i],
                    'shares': shares,
                    'price': stocks[i]["price"],
                    'transaction fees': transaction_fees,
                    'spent': actual_spent,
                    'weighted beta': stocks[i]['beta'] * (weights[i] / 100)
                }
                current_portfolio = pd.concat([current_portfolio, pd.DataFrame(new_row, index=[0])], ignore_index=True)
                
                # Add stock's daily value (shares * daily price) to the portfolio_values dataframe
                stock_values = stocks[i]["price_history"] * shares
                portfolio_values[stocks[i]["name"]] = stock_values
            
            # Compute portfolio total value
            portfolio_values['Portfolio'] = portfolio_values.sum(axis=1)
            
            # Calculate portfolio return from first day to final day when backtested on about a years worth of data
            portfolio_return = (
                portfolio_values['Portfolio'].iloc[-1] - portfolio_values['Portfolio'].iloc[0]
            ) / portfolio_values['Portfolio'].iloc[0]
            
            # Calculate portfolio daily returns and Sharpe ratio
            daily_returns = portfolio_values['Portfolio'].pct_change().dropna()
            avg_daily_return = daily_returns.mean()
            std_daily_return = daily_returns.std()
            sharpe_ratio = (avg_daily_return - risk_free_rate) / std_daily_return if std_daily_return > 0 else 0
            
            # Calculate portfolio beta
            portfolio_beta = current_portfolio['weighted beta'].sum()
            
            # Compute investment coefficient
            investment_coefficient = (20 * portfolio_beta) + (50 * avg_daily_return) + (30 * sharpe_ratio)
            
            # Check if this portfolio is the best for this number of stocks
            if investment_coefficient > best_invest_coeff:
                best_invest_coeff = investment_coefficient
                best_portfolio = current_portfolio.copy()
                best_portfolio_backtesting = portfolio_values.copy()
                best_portfolio["Portfolio Return"] = daily_returns
                best_portfolio["Sharpe Ratio"] = sharpe_ratio
                best_portfolio["Investment Coefficient"] = investment_coefficient

        # Store the best portfolio for this number of stocks
        strongest_portfolios[n] = best_portfolio
        back_testing_portfolios[n] = best_portfolio_backtesting
        
        # Add a summary row to the best portfolio
        final_row = {
            'Name': 'Total',
            'weight': best_portfolio['weight'].sum(),
            'shares': best_portfolio['shares'].sum(),
            'price': best_portfolio['price'].sum(),
            'transaction fees': best_portfolio['transaction fees'].sum(),
            'spent': best_portfolio['spent'].sum(),
            'weighted beta': portfolio_beta,
            'Portfolio Return': best_portfolio["Portfolio Return"].iloc[0],
            'Sharpe Ratio': best_portfolio["Sharpe Ratio"].iloc[0],
            'Investment Coefficient': best_invest_coeff
        }
        strongest_portfolios[n] = pd.concat([best_portfolio, pd.DataFrame(final_row, index=[0])], ignore_index=True)

    # Graphing the performance of the strongest portfolios and the benchmark
    
    return strongest_portfolios, back_testing_portfolios

""""""

def start(investment_size, min_stocks, max_stocks, flat_fee, fee_per_share, tickers):
    weighted_list, stock_data = rank(tickers)

    best_stocks = []
    for i in range(max_stocks):
        best_stocks += [weighted_list[i]["name"]]
    filtered_stocks = []
    for stock in best_stocks:
        for stock_stats in stock_data:
            if (stock == stock_stats["name"]):
                filtered_stocks += [stock_stats]
    for stock in filtered_stocks:
        stock["price_history"].index = stock["price_history"].index.strftime('%Y-%m-%d')

    best_portfolios, back_testing_portfolios = make_portfolios(filtered_stocks, investment_size, flat_fee, fee_per_share, min_stocks, max_stocks)

    return best_portfolios, back_testing_portfolios

@st.cache_data
def get_name_cached(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get('longName', "Unknown")
