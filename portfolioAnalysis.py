import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd

import finUtils


def getPortfolioData(portfolio):
    # check the weights
    if sum(portfolio.values()) != 1.0:
        raise ValueError('bad weights(s)')

    # retrieve the data
    data = yf.Tickers(' '.join(portfolio.keys())).history(period='max', progress=False)

    # check that all tickers were retrievable
    if any(data.isnull().all()):  # at least one column is entirely null
        # yfinance emits download error console messages for tickers it can't find but doesn't raise an exception. The
        # columns corresponding to a missing ticker have NaN values for every row.
        raise ValueError('bad ticker symbol(s)')

    # trim to the common time range and closing value columns
    return data['Close'].dropna()


def normalizePortfolioData(data):
    for column in data.columns:
        data[column] /= data[column].iloc[0]

    return data


# TODO: needed?
def combineTickers(d, weights):
    if sum(weights.values()) != 1.0:
        raise ValueError('bad weights')
    c = np.zeros_like(d[next(iter(d))])
    for key in weights:
        c += weights[key] * d[key]

    return c


# TODO: needed?
def generateFixedRateSeries(t, rAnnual):
    rDaily = finUtils.convAPRtoDay(rAnnual)
    s = np.zeros(t.shape)
    s[0] = 1.0
    for i in range(1, len(t)):
        delT = (t[i] - t[i - 1]).value / 86400e9
        s[i] = s[i - 1] * (1.0 + rDaily) ** delT

    return s


# TODO: needed?
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


weightsEye = {'VEMAX': 0.05,
              'VFIAX': 0.30,
              'VGSLX': 0.10,
              'VIPSX': 0.05,
              'VSMAX': 0.25,
              'VTMGX': 0.20,
              'VUSTX': 0.05}
weightsBogleYoung = {'VTSAX': 0.80,
                     'VBTLX': 0.20}
weightsExpenseTest = {'VUSTX': 0.5,
                      'VUSUX': 0.5}
# weightsBogleMiddle = {'VTSAX': 0.45,
#                       'VTIAX': 0.10,
#                       'VGSLX': 0.05,
#                       'VBTLX': 0.20,
#                       'VIPSX': 0.20}
# weightsBogleEarlyRet = {'VTSAX': 0.30,
#                         'VTIAX': 0.10,
#                         'VBTLX': 0.30,
#                         'VIPSX': 0.30}
# weightsBogleLateRet = {'VTSAX': 0.20,
#                        'VBTLX': 0.40,
#                        'VIPSX': 0.40}
# weightsSwedroeConvserv = {'VFIAX': 0.12,
#                           'VSMAX': 0.12,
#                           'VGSLX': 0.04,
#                           'VTMGX': 0.10,
#                           'VEMAX': 0.02,
#                           'VSBSX': 0.60}
# weightsSwedroeModerate = {'VFIAX': 0.18,
#                           'VSMAX': 0.18,
#                           'VGSLX': 0.06,
#                           'VTMGX': 0.15,
#                           'VEMAX': 0.03,
#                           'VSBSX': 0.40}
# weightsSwedroeModAggr = {'VFIAX': 0.24,
#                          'VSMAX': 0.24,
#                          'VGSLX': 0.08,
#                          'VTMGX': 0.20,
#                          'VEMAX': 0.04,
#                          'VSBSX': 0.20}
# weightsSwedroeHighAggr = {'VFIAX': 0.30,
#                           'VSMAX': 0.30,
#                           'VGSLX': 0.10,
#                           'VTMGX': 0.25,
#                           'VEMAX': 0.05,
#                           'VSBSX': 0.00}
  # U.S. Stocks: Large and Large Value -> VFIAX
  # U.S. Stocks: Small and Small Value -> VSMAX
  # U.S. Stocks: Real Estate -> VGSLX
  # Int'l Stocks: Large, Large Value, and Small -> VTMGX (VFSAX exists for small-cap, but has erratic/incomplete historical data)
  # Int'l Stocks: Emerging Markets -> VEMAX
  # U.S. Two-year -> VSBSX