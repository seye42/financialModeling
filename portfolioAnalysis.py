import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import string


# TODO: Should all of this be in a class so that all related data are more easily accessible?
# TODO: Document where the CSV data come from.

def parseTickerCSV(filename):
    # extract the ticker symbol
    path, name = os.path.split(filename)
    ticker = name.replace('.csv', '')
    
    # parse the date and closing value time series data
    df = pd.read_csv(filename)
    dates = pd.to_datetime(df['Date'].to_numpy())
    values = df['Close'].to_numpy()

    return (ticker, dates, values)


def parseAllTickerCSVs(filenames):
    # process each file
    tickers = []
    dates = []
    initialDates = []
    values = []
    for file in filenames:
        currTicker, currDates, currValues = parseTickerCSV(file)
        tickers.append(currTicker)
        dates.append(currDates)
        initialDates.append(currDates[0])
        values.append(currValues)

    # determine the limiting (latest) initial date
    startDate = max(initialDates)

    # trim the start of each time series to the common time and build up ticker dictionary
    d = {}
    for idx in range(len(tickers)):
        startIdx = np.searchsorted(dates[idx], startDate)
        if idx == 0:
            t = dates[idx][startIdx:]
        d[tickers[idx]] = values[idx][startIdx:]

    return (t, d)


def loadTimeSeries(filename, startTime):
    # parse
    d = pd.read_csv(filename)
    d['Time'] = pd.to_datetime(d['Date'])
    d['Value'] = d['Close']
    d = d.drop(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    # trim to starting time
    d = d[d['Time'] >= startTime]

    return d



files = ['/home/sean/Repos/financialModeling/data/VEMAX.csv',
         '/home/sean/Repos/financialModeling/data/VFIAX.csv',
         '/home/sean/Repos/financialModeling/data/VGSLX.csv',
         '/home/sean/Repos/financialModeling/data/VIPSX.csv',
         '/home/sean/Repos/financialModeling/data/VSMAX.csv',
         '/home/sean/Repos/financialModeling/data/VTMGX.csv',
         '/home/sean/Repos/financialModeling/data/VUSTX.csv']
#startTime = pd.to_datetime('2006-06-23')
weights = [0.05,
           0.30,
           0.10,
           0.05,
           0.25,
           0.20,
           0.05]

t, d = parseAllTickerCSVs(files)

matplotlib.rcParams.update({'font.size': 20, 'figure.facecolor': 'w', 'lines.linewidth': 2})
plt.figure()
for key in d.keys():
    plt.plot(t, d[key], label=key)
plt.xlabel('time')
plt.ylabel('closing value ($)')
plt.legend()
plt.grid()
