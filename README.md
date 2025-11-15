Sharpe Ratio Comparison App

Overview

The Sharpe Ratio Comparison App is a simple and interactive web application built with Streamlit. It allows users to calculate the Sharpe Ratio of a selected stock and compare it with the Nifty 500 index. This helps investors and analysts evaluate the risk-adjusted return performance of individual stocks relative to a benchmark.

The app uses  market data fetched via the yfinance  and performs financial computations using powerful Python libraries like pandas and numpy.

Features

Fetch live historical prices for any stock using yfinance.

Calculate  Sharpe Ratio for both the selected stock and the Nifty 500 index.

Visualize stock price  and performance comparisons interactively.

Simple web-based user interface built with Streamlit.

Tech Stack

Programming Language: Python

Framework: Streamlit

Libraries:

pandas – for data manipulation and analysis

numpy – for mathematical computations

yfinance – for market data retrieval


Usage

Enter the stock ticker symbol of your choice (e.g., TCS.NS, INFY.NS).


The app will:

Fetch historical price data for both the stock and Nifty 500 (^CRSLDX if using Yahoo Finance).

Compute daily returns and calculate Sharpe Ratios.


Future Improvements

Add multiple stock comparison.

Allow users to specify custom benchmarks.

Select the time frame.

Include risk-free rate input.

Add chart enhancements (rolling Sharpe Ratio, volatility plots).

