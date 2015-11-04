import csv
import sys
import pandas as pd
import collections


def update_symbol(ticker, ticker_dict, price, volume, time):
	'''Updates the MaxTimeGap, Volume, and MaxPrice of 
	trades for a given symbol, or ticker, and returns the
	ticker_dictionary with updates.'''
	tickdata = ticker_dict[ticker]
	max_time_gap = tickdata[0]
	total_vol = tickdata[1]
	wavg_price = tickdata[2]
	max_price = tickdata[3]
	last_timestamp = tickdata[4]
	if(time - last_timestamp > max_time_gap):
		max_time_gap = time - last_timestamp
	if(price > max_price):
		max_price = price
	wavg_price = (price*volume + wavg_price*total_vol)/(volume + total_vol)
	total_vol += volume
	last_timestamp = time
	ticker_dict[ticker] = [max_time_gap, total_vol, wavg_price, max_price, last_timestamp]
	return ticker_dict


def update_weighted_avgs(ticker_dict):
	'''Updates the WeightedAveragePrice for each
	symbol based upon price, volume pairs of trades
	stored in pricevolpairs.'''
	for ticker in ticker_dict:
		wavg = 0
		for pvpair in pricevolpairs[ticker]:
			wavg += pvpair[0]*pvpair[1]
		ticker_dict[ticker][2] = (int) (wavg / ticker_dict[ticker][1])
	return ticker_dict



'''The following code reads the csv file (from command line input) to a pandas
   dataframe with columns as listed. The file is then sorted primarily by 
   Symbol and secondarily by TimeStamp.'''
inp =  sys.argv[1]

pricevolpairs = collections.OrderedDict()
ticker_dict = collections.OrderedDict()
inpdata = pd.read_csv(inp, names=['TimeStamp', 'Symbol', 'Quantity', 'Price'], index_col=False)
inpdata1 = pd.read_csv(inp, iterator=True, chunksize=1024)
df = pd.concat(inpdata1,ignore_index=True)
df = inpdata.reindex(columns = ['Symbol', 'TimeStamp', 'Quantity', 'Price'])
temp_df = df.sort_index(0, ['Symbol', 'TimeStamp'])
final_df = temp_df.set_index(['Symbol'])


'''Iterates through all the rows in the file and either places the symbol into
   ticker_dictionary or updates the symbol's aggregated columns (i.e. total volume).
   Later writes the dictionary to an output csv
'''
for index, row in final_df.iterrows():
	if(index not in ticker_dict):
		ticker_dict[index] = [0, row.Quantity, row.Price, row.Price, row.TimeStamp]
		pricevolpairs[index] = [[row.Price, row.Quantity]]
	else:
		price = row.Price
		volume = row.Quantity
		time = row.TimeStamp
		pricevolpairs[index] += [[price, volume]]
		ticker_dict = update_symbol(index, ticker_dict, price, volume, time)

ticker_dict = update_weighted_avgs(ticker_dict)
result = pd.DataFrame.from_dict(ticker_dict, orient='index')
result = result.drop(4, axis=1)
result.columns = ['MaxTimeGap','Volume','WeightedAveragePrice','MaxPrice']
result.to_csv('output.csv', header=False, chunksize=1024, sep=',')
