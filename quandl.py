import Quandl
import pandas


def closing(tickarr):
	queryarr = ['YAHOO/%s' % tick for tick in tickarr] #.4 is for closing price column concatination
	closingdata = Quandl.get(queryarr, trim_start='2001-01-01', authtoken="H4uWGQ3jQdm96V7H2Abm") #trimming start date...
	#print(closingdata)
	closingdata.to_csv('out2.csv', sep='\t')
	#print(closingdata)
	#for tick in tickarr:
	#	print("YAHOO/%s" % tick)
	#	tickclosing = Quandl.get("YAHOO/%s.4" % tick)
	#	print(tickclosing)
tickers = ["AAPL", "GOOG", "IBM"]
closing(tickers)