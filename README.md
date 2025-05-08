# PortfolioGo - Your Robo-Advisor

PortfolioGo! is a robo-advisor designed to assist users in simulating and optimizing investment portfolios. It provides tools for portfolio creation, backtesting, and optimization using **real-time** financial data.

TRY IT HERE: https://portfoliogo.streamlit.app

## Features

- **Portfolio Simulation**: Create and simulate portfolios based on user-defined constraints.
- **Backtesting**: Evaluate portfolio performance using historical data.
- **Optimization**: Optimize portfolios using financial metrics like the Sharpe ratio, Beta, and Expected Return.
- **Interactive UI**: Built with Streamlit for an intuitive and interactive user experience.
- **Customizable Parameters**: Define investment constraints such as total investment size, minimum/maximum stocks, and transaction fees.

## Project Structure

- **`app.py`**: Main entry point for the application.
- **`stocks.py`**: Manages input of stocks.
- **`clean.py`**: Prepares and validates stock data.
- **`param.py`**: Handles user input for investment parameters (investment size, transaction fees).
- **`result.py`**: Displays portfolio results and analysis.
- **`generate.py`**: Contains logic for generating portfolios.
- **`helpers.py`**: Utility functions for data processing.
- **`components.py`**: Contains reusable UI components like headers and footers.

## Usage
Head to https://portfoliogo.streamlit.app and give it a try! No accounts, payments, or waiting required.

**NOTE:** Occasionaly, the yfinance library (which is used in the back-end to fetch stock data) experiences issues which result in the program becoming unresponsive. This is an unfortunate consequnce of using real-time data and we will always try to minimize disruption on our end.

## Data Sources
Data for this project is obtained from the yfinance library, for real-time financial data.

## Disclaimer
This project is for educational purposes only. Always consult a financial advisor/use personal judgement before making investment decisions.
