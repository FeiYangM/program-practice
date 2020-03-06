#!/usr/bin/env python
# coding: utf-8


##usage : python momentum_trade.py price_file top_number
##        price file should be like this:
##				date,ticker,adj_close
##				2010-1-1,A,29.1
##				2010-1-2,A,29.2
##				...............
##				2015-1-1,B,52.2
##				...............
##				2016-1-1,Z,35.2
##
##			top_number:
##				Half of the number you want to be included in your portfolio. 
##				For example:
##					if the number is 10, the program will choose top 
##					10 stocks and bottom 10 stocks to be your portfolio.
##

import sys
import pandas as pd
import numpy as np

from scipy import stats

def read_data(file):
	#read data and pivot based on date
	data = pd.read_csv(file, parse_dates = ['date'], index_col = False)
	close = data.reset_index().pivot(index = 'date', columns = 'ticker', values = 'adj_close')
	return close

def resample_price(price, freq):
	return price.resample(freq).last() #transfer to monthly based and the price is the last one

def log_returns(price): # calculate log retunrs
	return (np.log(price / price.shift(1)))

def shift_returns(returns, shift_n):
	return returns.shift(shift_n)

def get_topN(previous_returns, topN): # choose the stocks with top highest returns
	top_stocks = previous_returns.copy()
	for i, values in previous_returns.iterrows():
		top = values.nlargest(topN).index
		top_stocks.loc[i] = 0
		top_stocks.loc[i, top] = 1
		top_stocks = top_stocks.astype(bool).astype('int64')
	return top_stocks

def portfolio_returns(df_long, df_short, lookahead_returns, n_stocks): 
	#estimate the portfolio returns
	portfolio = df_long - df_short
	returns = portfolio * lookahead_returns / n_stocks

	return returns

def t_test(expected_portfolio_returns_bydate):
	# t-test for the expected returns
	t_score, p_score = stats.ttest_1samp(expected_portfolio_returns_bydate, 0.0)

	return t_score, p_score / 2

if __name__ == '__main__':
	close_prices = read_data(sys.argv[1])
	monthly_close = resample_price(close_prices, 'M')
	monthy_close_returns = log_returns(monthly_close)

	previous_returns = shift_returns(monthy_close_returns, 1)# previous month
	lookahead_returns = shift_returns(monthy_close_returns, -1)# one month ahead


	# calculate top N and bottom N for stocks
	N = int(sys.argv[2])
	df_long = get_topN(previous_returns, N)
	df_short = get_topN(-1 * previous_returns, N)

	#calculate portfolio info
	expected_portfolio_returns = portfolio_returns(df_long, df_short, lookahead_returns, 2 * N)	
	expected_portfolio_returns_bydate = expected_portfolio_returns.T.sum().dropna()

	portfolio_mean = expected_portfolio_returns_bydate.mean()
	portfolio_ste = expected_portfolio_returns_bydate.sem()
	portfolio_annual = (np.exp(portfolio_mean * 12) - 1) * 100

	t_value, p_value = t_test(expected_portfolio_returns_bydate)

	#you can add more code if you want to print more info
	print("Annual Rate of Return : {:.2f}%".format(portfolio_annual))
	print(t_value, p_value)
	

	# uncomment the code below if you want to take a look at the expected_portfolio_returns_bydate
	# you can also output it to a file
	#print(expected_portfolio_returns_bydate)




