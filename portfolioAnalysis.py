import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd

import finUtils

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


def generateFixedRateSeries(t, rAnnual):
    rDaily = finUtils.convAPRtoDay(rAnnual)
    s = np.zeros(t.shape)
    s[0] = 1.0
    for i in range(1, len(t)):
        delT = (t[i] - t[i - 1]).value / 86400e9
        s[i] = s[i - 1] * (1.0 + rDaily) ** delT

    return s


def includeFees(t, s, rAnnual):
    rDaily = finUtils.convAPRtoDay(rAnnual)
    corr = 1.0
    c = np.zeros(s.shape)
    c[0] = s[0]
    for i in range(1, len(t)):
        delT = (t[i] - t[i - 1]).value / 86400e9
        corr *= (1.0 + rDaily) ** delT
        c[i] = s[i] * corr

    return c


files = ['/home/sean/Repos/financialModeling/data/VEMAX.csv',
         '/home/sean/Repos/financialModeling/data/VFIAX.csv',
         '/home/sean/Repos/financialModeling/data/VGSLX.csv',
         '/home/sean/Repos/financialModeling/data/VIPSX.csv',
         '/home/sean/Repos/financialModeling/data/VSMAX.csv',
         '/home/sean/Repos/financialModeling/data/VTMGX.csv',
         '/home/sean/Repos/financialModeling/data/VUSTX.csv',
         #'/home/sean/Repos/financialModeling/data/VLXVX.csv',
         #'/home/sean/Repos/financialModeling/data/VTTSX.csv',
         '/home/sean/Repos/financialModeling/data/VFFVX.csv',
         #'/home/sean/Repos/financialModeling/data/FDEEX.csv',
         #'/home/sean/Repos/financialModeling/data/FFFHX.csv',
         '/home/sean/Repos/financialModeling/data/VTIAX.csv',
         '/home/sean/Repos/financialModeling/data/VBTLX.csv',
         '/home/sean/Repos/financialModeling/data/VTSAX.csv',
         '/home/sean/Repos/financialModeling/data/VSBSX.csv',
         '/home/sean/Repos/financialModeling/data/VGLT.csv',
         '/home/sean/Repos/financialModeling/data/VMBS.csv',
         '/home/sean/Repos/financialModeling/data/VGIT.csv',
         '/home/sean/Repos/financialModeling/data/VGSH.csv',
         '/home/sean/Repos/financialModeling/data/SCHP.csv',
         '/home/sean/Repos/financialModeling/data/USIG.csv',
         '/home/sean/Repos/financialModeling/data/SPSM.csv',
         '/home/sean/Repos/financialModeling/data/IEMG.csv',
         '/home/sean/Repos/financialModeling/data/IWY.csv',
         '/home/sean/Repos/financialModeling/data/IWX.csv',
         '/home/sean/Repos/financialModeling/data/EFG.csv',
         '/home/sean/Repos/financialModeling/data/EFV.csv',
         '/home/sean/Repos/financialModeling/data/IWP.csv',
         '/home/sean/Repos/financialModeling/data/IWS.csv',
         '/home/sean/Repos/financialModeling/data/PRWCX.csv',
         '/home/sean/Repos/financialModeling/data/VINIX.csv',
         '/home/sean/Repos/financialModeling/data/FCNTX.csv',
         '/home/sean/Repos/financialModeling/data/VMCIX.csv',
         '/home/sean/Repos/financialModeling/data/VSCIX.csv',
         '/home/sean/Repos/financialModeling/data/VWINX.csv',
         '/home/sean/Repos/financialModeling/data/VGHCX.csv']

weightsEye = {'VEMAX': 0.05,
              'VFIAX': 0.30,
              'VGSLX': 0.10,
              'VIPSX': 0.05,
              'VSMAX': 0.25,
              'VTMGX': 0.20,
              'VUSTX': 0.05}
weightsBro = {'VMFXX': 0.0192,
              'VGHCX': 0.029,
              'VIPSX': 0.021,
              'VGSLX': 0.023,
              'VTSAX': 0.0264,
              'VWINX': 0.0266,
              'VSCIX': 0.0758,
              'VMCIX': 0.0565,
              'FCNTX': 0.0942,
              'VINIX': 0.0385,
              'PRWCX': 0.0798,
              'FR1': 0.2636,
              'FR2': 0.0029,
              'IWS': 0.0136,
              'IWP': 0.007,
              'EFV': 0.014,
              'EFG': 0.0098,
              'IWX': 0.0226,
              'IWY': 0.0305,
              'IEMG': 0.0084,
              'SPSM': 0.0102,
              'USIG': 0.0178,
              'SCHP': 0.0022,
              'VGSH': 0.0118,
              'VGIT': 0.012,
              'VMBS': 0.0188,
              'VGLT': 0.0047,
              'VFIAX': 0.0601}
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
#weightsSwedroeConvserv = {'VFIAX': 0.12,
#                          'VSMAX': 0.12,
#                          'VGSLX': 0.04,
#                          'VTMGX': 0.10,
#                          'VEMAX': 0.02,
#                          'VSBSX': 0.60}
#weightsSwedroeModerate = {'VFIAX': 0.18,
#                          'VSMAX': 0.18,
#                          'VGSLX': 0.06,
#                          'VTMGX': 0.15,
#                          'VEMAX': 0.03,
#                          'VSBSX': 0.40}
#weightsSwedroeModAggr = {'VFIAX': 0.24,
#                         'VSMAX': 0.24,
#                         'VGSLX': 0.08,
#                         'VTMGX': 0.20,
#                         'VEMAX': 0.04,
#                         'VSBSX': 0.20}
#weightsSwedroeHighAggr = {'VFIAX': 0.30,
#                          'VSMAX': 0.30,
#                          'VGSLX': 0.10,
#                          'VTMGX': 0.25,
#                          'VEMAX': 0.05,
#                          'VSBSX': 0.00}
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

# generate fixed-rate "funds"
d['VMFXX'] = generateFixedRateSeries(t, 0.0)  # Vanguard Federal Money Market Fund
d['FR1'] = generateFixedRateSeries(t, 0.0309)  # KPERS Stable Value
d['FR2'] = generateFixedRateSeries(t, 0.0013)  # FDIC Bank Deposit Sweep

# simulate custom portfolios
c= {}
c['Eye'] = combineTickers(d, weightsEye)
c['Broslavick'] = combineTickers(d, weightsBro)
c['Broslavick (with JAG fees)'] = includeFees(t, c['Broslavick'], -0.015 * 0.19)
c['Bogleheads Young'] = combineTickers(d, weightsBogleYoung)
c['Bogleheads Middle'] = combineTickers(d, weightsBogleMiddle)
c['Bogleheads Early Retirement'] = combineTickers(d, weightsBogleEarlyRet)
c['Bogleheads Late Retirement'] = combineTickers(d, weightsBogleLateRet)
#c['Swedroe Conservative'] = combineTickers(d, weightsSwedroeConvserv)
#c['Swedroe Moderate'] = combineTickers(d, weightsSwedroeModerate)
#c['Swedroe Moderately Aggressive'] = combineTickers(d, weightsSwedroeModAggr)
#c['Swedroe Highly Aggressive'] = combineTickers(d, weightsSwedroeHighAggr)
#c['Vanguard Target 2065'] = d['VLXVX']
#c['Vanguard Target 2060'] = d['VTTSX']
c['Vanguard Target 2055'] = d['VFFVX']
#c['Fidelity Target 2055'] = d['FDEEX']
#c['Fidelity Target 2050'] = d['FFFHX']

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