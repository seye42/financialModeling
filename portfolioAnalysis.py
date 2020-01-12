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
        print(currTicker + ' ' + str(currDates[0]))

    # determine the limiting date range across all tickers
    startDate = max(initialDates)
    stopDate = min(finalDates)
    print('keeping ' + str(startDate) + ' to ' + str(stopDate))

    # trim the time span of each series and build up the ticker dictionary
    d = {}
    for i in range(len(tickers)):
        startIdx = np.searchsorted(dates[i], startDate)
        stopIdx = np.searchsorted(dates[i], stopDate)
        if i == 0:
            t = dates[i][startIdx:stopIdx]
        d[tickers[i]] = values[i][startIdx:stopIdx]

    return (t, d)


def combineTickers(d, weights):
    if sum(weights.values()) != 1.0:
        raise ValueError('bad weights')
    c = np.zeros_like(d[next(iter(d))])
    for key in weights:
        c += weights[key] * d[key]

    return c


files = ['/home/sean/Repos/financialModeling/data/VEMAX.csv',
         '/home/sean/Repos/financialModeling/data/VFIAX.csv',
         '/home/sean/Repos/financialModeling/data/VGSLX.csv',
         '/home/sean/Repos/financialModeling/data/VIPSX.csv',
         '/home/sean/Repos/financialModeling/data/VSMAX.csv',
         '/home/sean/Repos/financialModeling/data/VTMGX.csv',
         '/home/sean/Repos/financialModeling/data/VUSTX.csv',
         #'/home/sean/Repos/financialModeling/data/VLXVX.csv',
         #'/home/sean/Repos/financialModeling/data/FDEEX.csv',
         #'/home/sean/Repos/financialModeling/data/FFFHX.csv',
         '/home/sean/Repos/financialModeling/data/VBTLX.csv',
         '/home/sean/Repos/financialModeling/data/VTSAX.csv',
         '/home/sean/Repos/financialModeling/data/VTIAX.csv',
         '/home/sean/Repos/financialModeling/data/VSBSX.csv']

weightsEye = {'VEMAX': 0.05,
              'VFIAX': 0.30,
              'VGSLX': 0.10,
              'VIPSX': 0.05,
              'VSMAX': 0.25,
              'VTMGX': 0.20,
              'VUSTX': 0.05}
weightsBogleYoung = {'VTSAX': 0.80,
                     'VBTLX': 0.20}
weightsBogleMiddle = {'VTSAX': 0.45,
                     'VTIAX': 0.10,
                     'VGSLX': 0.05,
                     'VBTLX': 0.20,
                     'VIPSX': 0.20}
weightsBogleEarlyRet = {'VTSAX': 0.30,
                       'VTIAX': 0.10,
                       'VBTLX': 0.30,
                       'VIPSX': 0.30}
weightsBogleLateRet = {'VTSAX': 0.20,
                       'VBTLX': 0.40,
                       'VIPSX': 0.40}
weightsSwedroeConvserv = {'VFIAX': 0.12,
                          'VSMAX': 0.12,
                          'VGSLX': 0.04,
                          'VTMGX': 0.10,
                          'VEMAX': 0.02,
                          'VSBSX': 0.60}
weightsSwedroeModerate = {'VFIAX': 0.18,
                          'VSMAX': 0.18,
                          'VGSLX': 0.06,
                          'VTMGX': 0.15,
                          'VEMAX': 0.03,
                          'VSBSX': 0.40}
weightsSwedroeModAggr = {'VFIAX': 0.24,
                         'VSMAX': 0.24,
                         'VGSLX': 0.08,
                         'VTMGX': 0.20,
                         'VEMAX': 0.04,
                         'VSBSX': 0.20}
weightsSwedroeHighAggr = {'VFIAX': 0.30,
                          'VSMAX': 0.30,
                          'VGSLX': 0.10,
                          'VTMGX': 0.25,
                          'VEMAX': 0.05,
                          'VSBSX': 0.00}
  # U.S. Stocks: Large and Large Value -> VFIAX
  # U.S. Stocks: Small and Small Value -> VSMAX
  # U.S. Stocks: Real Estate -> VGSLX
  # Int'l Stocks: Large, Large Value, and Small -> VTMGX (VFSAX exists for small-cap, but has erratic/incomplete historical data)
  # Int'l Stocks: Emerging Markets -> VEMAX
  # U.S. Two-year -> VSBSX

# parse the historical time series data
t, dUnnorm = parseAllTickerCSVs(files)

# normalize to starting dollars (not price per share)
d = {}
for key in dUnnorm:
    d[key] = dUnnorm[key] / dUnnorm[key][0]

# simulate custom portfolios
c= {}
c['Eye'] = combineTickers(d, weightsEye)
c['Bogleheads Young'] = combineTickers(d, weightsBogleYoung)
c['Bogleheads Middle'] = combineTickers(d, weightsBogleMiddle)
c['Bogleheads Early Retirement'] = combineTickers(d, weightsBogleEarlyRet)
c['Bogleheads Late Retirement'] = combineTickers(d, weightsBogleLateRet)
c['Swedroe Conservative'] = combineTickers(d, weightsSwedroeConvserv)
c['Swedroe Moderate'] = combineTickers(d, weightsSwedroeModerate)
c['Swedroe Moderately Aggressive'] = combineTickers(d, weightsSwedroeModAggr)
c['Swedroe Highly Aggressive'] = combineTickers(d, weightsSwedroeHighAggr)

# plot closing values
matplotlib.rcParams.update({'font.size': 20, 'figure.facecolor': 'w', 'lines.linewidth': 2})
plt.figure()
for key in dUnnorm:
    plt.plot(t, dUnnorm[key], label=key)
plt.xlabel('time')
plt.ylabel('closing value ($)')
plt.legend()
plt.grid()

# plot normalized values of core funds
plt.figure()
for key in d.keys():
    plt.plot(t, d[key], label=key)
plt.xlabel('time')
plt.ylabel('normalized value')
plt.legend()
plt.grid()

# plot normalized values of weighted portfolios
plt.figure()
for key in c.keys():
    plt.plot(t, c[key], label=key)
plt.xlabel('time')
plt.ylabel('normalized value')
plt.legend()
plt.grid()