import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd

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
    finalDates = []
    values = []
    for file in filenames:
        currTicker, currDates, currValues = parseTickerCSV(file)
        tickers.append(currTicker)
        dates.append(currDates)
        initialDates.append(currDates[0])
        finalDates.append(currDates[-1])
        values.append(currValues)

    # determine the limiting date range across all tickers
    startDate = max(initialDates)
    stopDate = min(finalDates)

    # trim the start of each time series to the common time and build up ticker dictionary
    d = {}
    for idx in range(len(tickers)):
        startIdx = np.searchsorted(dates[idx], startDate)
        stopIdx = np.searchsorted(dates[idx], stopDate)
        if idx == 0:
            t = dates[idx][startIdx:stopIdx]
        d[tickers[idx]] = values[idx][startIdx:stopIdx]

    return (t, d)


files = ['/home/sean/Repos/financialModeling/data/VEMAX.csv',
         '/home/sean/Repos/financialModeling/data/VFIAX.csv',
         '/home/sean/Repos/financialModeling/data/VGSLX.csv',
         '/home/sean/Repos/financialModeling/data/VIPSX.csv',
         '/home/sean/Repos/financialModeling/data/VSMAX.csv',
         '/home/sean/Repos/financialModeling/data/VTMGX.csv',
         '/home/sean/Repos/financialModeling/data/VUSTX.csv',
         #'/home/sean/Repos/financialModeling/data/VLXVX.csv']
         #'/home/sean/Repos/financialModeling/data/FDEEX.csv']
         '/home/sean/Repos/financialModeling/data/FFFHX.csv']
weights = {'VEMAX': 0.05,
           'VFIAX': 0.30,
           'VGSLX': 0.10,
           'VIPSX': 0.05,
           'VSMAX': 0.25,
           'VTMGX': 0.20,
           'VUSTX': 0.05}

t, d = parseAllTickerCSVs(files)

# simulate custom portfolio
d['Custom'] = np.zeros_like(d[next(iter(d))])
for key in weights:
    d['Custom'] += weights[key] * d[key]

# plot closing values
matplotlib.rcParams.update({'font.size': 20, 'figure.facecolor': 'w', 'lines.linewidth': 2})
plt.figure()
for key in d:
    plt.plot(t, d[key], label=key)
plt.xlabel('time')
plt.ylabel('closing value ($)')
plt.legend()
plt.grid()

# plot normalized values
nd = {}
for key in d:
    nd[key] = d[key] / d[key][0]

plt.figure()
for key in d.keys():
    plt.plot(t, nd[key], label=key)
plt.xlabel('time')
plt.ylabel('normalized value')
plt.legend()
plt.grid()
