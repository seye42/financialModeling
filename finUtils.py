import math
import numpy as np
import plotUtils


def convAPRtoDay(rAnnual):
    '''
    Convert APR to equivalent daily rate
    '''

    # preserve sign of negative rates to indicate discount calculations later
    sign = np.sign(rAnnual)
    rAnnual = np.fabs(rAnnual)

    # solve (1 + rAnnual) = (1 + rDaily) ** 365
    rDaily = (1.0 + rAnnual) ** (1.0 / 365.0) - 1.0

    return sign * rDaily


def convAPRtoMon(rAnnual):
    '''
    Convert APR to equivalent monthly rate
    '''

    # preserve sign of negative rates to indicate discount calculations later
    sign = np.sign(rAnnual)
    rAnnual = np.fabs(rAnnual)

    # solve (1 + rAnnual) = (1 + rMonthly) ** 12
    rMonthly = (1.0 + rAnnual) ** (1.0 / 12.0) - 1.0

    return sign * rMonthly


def compoundInt(P, r):
    '''
    Calculate compound interest
    '''

    if r >= 0.0:  # appreciation
        F = P * (1.0 + r)
    else:  # depreciation
        F = P / (1.0 + np.fabs(r))

    return F


def timeSeries(params, accounts):
    # build age array
    ages = np.arange(params['startAge'], params['stopAge'], 1.0 / 12)
        # in years, but always with monthly steps

    # figure out where December falls in the age array (for RMD calculations)
    fracMo, _ = math.modf(params['startAge'])
    nextDecIdx = 12 - (params['birthMonth'] + int(round(fracMo * 12.0))) % 12
        # month for integer ages plus fractional year (converted to month indices)

    # initialize aggregate time series arrays
    earnedIncomes   = np.zeros_like(ages)
    totalIncomes    = np.zeros_like(ages)
    expenses        = np.zeros_like(ages)
    discretionaries = np.zeros_like(ages)
    netWorths       = np.zeros_like(ages)

    # initialize accounts
    for a in accounts:
        # setup balances time series
        if 'hasBalance' in a:
            # convert APR to monthly rate
            a['intMonthly'] = convAPRtoMon(a['intAPR'])

            # setup balances and adjust net worth
            a['balances'] = np.zeros_like(ages)
            a['balances'][0] = a['initBalance']
            netWorths[0] += a['initBalance']

        # setup payments time series
        a['payments'] = np.zeros_like(ages)

        # setup previous December's balance for later RMD calculations
        if 'hasRMDs' in a:
             a['prevDecBalance'] = a['initBalance']  # best estimate for now, will be updated below

    # run time series calculations
    for idx in range(1, len(ages)):  # skip the first age since it's just initial value data
        # accrue interest
        for a in accounts:
            if 'hasBalance' in a:  # interest bearing account
                a['balances'][idx] = compoundInt(a['balances'][idx - 1], a['intMonthly'])

        # add contributions
        # TODO: add another check for when RMDs kick in (regardless of maxAge)?
        for a in accounts:
            if 'hasContributions' in a:  # defined contribution account
                if ages[idx] >= a['minAge'] and ages[idx] <= a['maxAge']:  # active contribution
                    a['payments'][idx] = a['delMonthly']
                    a['balances'][idx] += a['delMonthly']

        # get total income and expenses
        for a in accounts:
            if 'hasIncome' in a:
                if ages[idx] >= a['minAge'] and ages[idx] <= a['maxAge']:  # active income stream
                    a['payments'][idx] = a['delMonthly']
                    if a['earned']:
                        earnedIncomes[idx] += a['delMonthly']
                    totalIncomes[idx]  += a['delMonthly']
            elif 'hasRMDs' in a:
                RMD = getReqMinDistrib(ages[idx], a['prevDecBalance'])
                if RMD > 0.0:
                    payment = min([a['balances'][idx - 1], RMD])
                    a['payments'][idx] = -payment  # withdrawals are negative
                    a['balances'][idx] -= payment  # withdrawals are negative
                    totalIncomes[idx] += payment
            elif 'hasExpenses' in a:
                if ages[idx] >= a['minAge'] and ages[idx] <= a['maxAge']:  # active expense stream
                    a['payments'][idx] = a['delMonthly']
                    expenses[idx] += a['delMonthly']

        # determine net cash flow
        discretionaries[idx] = totalIncomes[idx] + expenses[idx]
        avail = discretionaries[idx]

        # use positive cash flow on accounts with contribution limits and then savings spillover
        if avail > 0.0:
            # maximize Roth IRA contributions
            # TODO: switch to getRothContrib() with separately calculated earned and Roth AGI incomes
            if avail > 0.0:
                earnedAvail = earnedIncomes[idx]
                for a in accounts:
                    if 'hasContributionLimits' in a:
                        # incomes
                        contrib = min([earnedAvail, avail, a['maxContrib']])
                            # can't contribute unless there's earned income to cover it
                        a['balances'][idx] += contrib
                        a['payments'][idx] += contrib
                        earnedAvail -= contrib
                        avail -= contrib

            # add whatever remains to savings
            if avail > 0.0:
                for a in accounts:
                    if 'hasSavings' in a:
                        a['balances'][idx] += avail
                        a['payments'][idx] += avail
                        avail = 0.0
                        break  # only the first account with hasSavings is used

        # tap prioritized list of savings to address negative cash flow
        elif avail < 0.0:
            # withdraw from general savings
            # TODO: estimate capital gains realizations
            for a in accounts:
                if 'hasSavings' in a and a['balances'][idx] > 0.0:  # savings with an available balance
                    withdraw = min([-avail, a['balances'][idx]])
                    a['balances'][idx] -= withdraw
                    a['payments'][idx] -= withdraw
                    avail += withdraw  # avail is negative

            # withdraw from accounts subject to RMDs
            # TODO: account for optional withdrawals to reduce RMDs in future time steps
            if avail < 0.0:
                for a in accounts:
                    if 'hasRMDs' in a and a['balances'][idx] > 0.0:  # IRA or 401(k) with an available balance
                        withdraw = min([-avail, a['balances'][idx]])
                        a['balances'][idx] -= withdraw
                        a['payments'][idx] -= withdraw
                        avail += withdraw  # avail is negative
                        totalIncomes[idx] += withdraw  # distributions are normal income for tax purposes

            # withdraw from other balance-holding accounts in order
            # TODO: add support for HSAs that can't be used to cover general expenses
            if avail < 0.0:
                for a in accounts:
                    if 'hasBalance' in a and a['balances'][idx] > 0.0:
                        withdraw = min([-avail, a['balances'][idx]])
                        a['balances'][idx] -= withdraw
                        a['payments'][idx] -= withdraw
                        avail += withdraw  # avail is negative
                        totalIncomes[idx] += withdraw  # distributions are normal income for tax purposes
                          # the unique hasSavings account will have a zeroed balance here

        # calculate net worth
        for a in accounts:
            if 'hasBalance' in a:
                netWorths[idx] += a['balances'][idx]

        # update end-of-December tracking for IRA RMDs
        if idx == nextDecIdx:  # it's December, save balances (with new interest) for use next year
            nextDecIdx += 12
            for a in accounts:
                if 'hasRMDs' in a:
                    a['prevDecBalance'] = a['balances'][idx]

    # plot aggregate incomes and expenses
    plotUtils.multiPlot(ages, [earnedIncomes, totalIncomes, expenses, discretionaries],
                        'age (yr)', 'rate (' + params['currencyYear'] + ' $/mo)',
                        ['earned income', 'total income', 'total expenses', 'discretionary'])

    # plot accounts with balances
    balances = []
    names = []
    doPlot = False
    for a in accounts:
        if 'balances' in a:
            doPlot = True
            balances.append(a['balances'])
            names.append(a['label'])
    if doPlot:
        plotUtils.multiPlot(ages, balances, 'age (yr)', 'balance (' + params['currencyYear'] + ' $)', names)

    # plot contributions and payments
    payments = []
    names = []
    doPlot = False
    for a in accounts:
        if 'payments' in a:
            doPlot = True
            payments.append(a['payments'])
            names.append(a['label'])
    if doPlot:
        plotUtils.multiPlot(ages, payments, 'age (yr)', 'payments (' + params['currencyYear'] + ' $/mo)', names)

    # plot net worth
    plotUtils.singlePlot(ages, netWorths, 'age (yr)', 'net worth (' + params['currencyYear'] + ' $)')

    return accounts


def getRothContrib(totalIncome, earnedIncome, maxContrib, phaseOutBeg, phaseOutEnd):
    '''
    Get the allowable Roth IRA contribution according to IRS rules for phase-out and income limits.

    Calculations are based on IRS publication 590-A, Worksheet 2-2 from 2017 (ignoring some minor rounding and minimum
    rules on the final value)
    '''

    if totalIncome < phaseOutBeg:  # contribution limited only by earned income
        contrib = min([earnedIncome, maxContrib])
    elif totalIncome < phaseOutEnd: # contribution limited by phase-out rules
        mult = (phaseOutEnd - totalIncome) /  (phaseOutEnd - phaseOutBeg)
        contrib = mult * min([earnedIncome, maxContrib])
    else:  # ineligible for Roth contributions, income is too high
        contrib = 0.0

    return contrib


def getReqMinDistrib(age, P):
    '''
    Get the required minimum distribution for an IRA or 401(k) according to IRS rules. Returned RMDs are normalized to
    monthly amounts.
    - age is the account holder's current age in years
    - P is the account balance/principal as of 31 Dec the previous year

    Calculations are based on IRS publication 590-B, Table III from 2019
    '''

    '''
    Technically, rules allow for first RMD to occur by 1 Apr of the year following the one in which the person turns
    70.5. This can sometimes forestall when the first distribution must be taken for people with birthdays in the
    first half of the year. The IRS rule wording is a little unclear about whether a second withdrawal needs to occur
    in that same year. The simplifying assumption used here is that the first RMD is taken the year the account holder
    age is 70 and proceeds normally on a monthly basis thereafter.
    '''

    # TODO: Update based on SECURE Act of 2019 increased age of 72
    print('getReqMinDistrib() not updated for SECURE Act of 2019')

    # previous balance divisor
    d = [27.4,  # age 70
         26.5,
         25.6,
         24.7,
         23.8,
         22.9,
         22.0,
         21.2,
         20.3,
         19.5,
         18.7,  # age 80
         17.9,
         17.1,
         16.3,
         15.5,
         14.8,
         14.1,
         13.4,
         12.7,
         12.0,
         11.4,  # age 90
         10.8,
         10.2,
         9.6,
         9.1,
         8.6,
         8.1,
         7.6,
         7.1,
         6.7,
         6.3,  # age 100
         5.9,
         5.5,
         5.2,
         4.9,
         4.5,
         4.2,
         3.9,
         3.7,
         3.4,
         3.1,  # age 110
         2.9,
         2.6,
         2.4,
         2.1,
         1.9]  # 115 and over
      # from IRS publication 590-B, Table III, 2019

    # calculate the required minimum distribution
    if age < 70.0:
        RMD = 0.0
    elif age >= 115.0:
        RMD = P / d[-1] / 12.0  # 12: convert annual RMD to a monthly value
    else:
        idx = int(math.floor(age) - 70)
        RMD = P / d[idx] / 12.0

    return RMD