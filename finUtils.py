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

    # figure out where Dec falls in the age array (for IRA and 401(k) RMDs)
    fracMo, _ = math.modf(params['startAge'])
    nextDecIdx = 12 - (params['birthMonth'] + int(round(fracMo * 12.0))) % 12
        # month for integer ages plus fractional year (converted to month indices)

    # initialize aggregate time series arrays
    incomes  = np.zeros_like(ages)
    expenses = np.zeros_like(ages)
    discret  = np.zeros_like(ages)
    netWorth = np.zeros_like(ages)

    # initialize accounts
    for a in accounts:
        if 'adjAPR' in a:  # income type
            # convert APR to monthly rate
            a['adjMonthly'] = convAPRtoMon(a['adjAPR'])

            # initialize time series
            a['payments'] = np.zeros_like(ages)
            if ages[0] >= a['minAge'] and ages[0] <= a['maxAge']:  # active income stream
                a['payments'][0] = a['delMonthly']
        elif 'intAPR' in a:  # loan, savings, IRA, 401(k), Roth, Roth 401(k), or HSA type
            # convert APR to monthly rate
            a['intMonthly'] = convAPRtoMon(a['intAPR'])

            # initialize time series and net worth
            a['payments'] = np.zeros_like(ages)
            a['balances'] = np.zeros_like(ages)
            a['balances'][0] = a['initBalance']
            netWorth[0] += a['initBalance']

            # initialize previous Dec's balance for RMD calculations on IRAs and 401(k)s
            if a['type'] in ['IRA', '401(k)']:
                a['prevDecBalance'] = a['initBalance']
                    # best estimate for now, will be updated below

    # run time series calculations
    for idx in range(1, len(ages)):  # skip the first age since it's just initial value data
        # get total income and expenses for this period
        for a in accounts:
            if a['type'] == 'income':
                if ages[idx] >= a['minAge'] and ages[idx] <= a['maxAge']:  # active income stream
                    if ages[idx - 1] < a['minAge']:  # previous time step was outside of age bounds
                        # first month of this income stream, use initial value
                        payment = a['delMonthly']
                            # TODO: think about inflation adjusting income streams (e.g. SS)
                    else:  # ongoing income, adjust previous month's payment based on compound rate
                        payment = compoundInt(a['payments'][idx - 1], a['adjMonthly'])
                    a['payments'][idx] = payment
                    incomes[idx] += payment
                else:  # age is outside of bounds, inactive income stream
                    a['payments'][idx] = 0.0
            elif a['type'] in ['IRA', '401(k)']:
                payment = getReqMinDistrib(ages[idx], a['prevDecBalance'])
                a['payments'][idx] = -payment  # withdrawals are negative
                incomes[idx] += payment
            elif a['type'] == 'expense':
                if ages[idx] >= a['minAge'] and ages[idx] <= a['maxAge']:  # active expense stream
                    if ages[idx - 1] < a['minAge']:  # previous time step was outside of age bounds
                        # first month of this expense stream, use initial value
                        payment = a['delMonthly']
                    else:  # ongoing expense, adjust previous month's payment based on compound rate
                        payment = compoundInt(a['payments'][idx - 1], a['adjMonthly'])
                    a['payments'][idx] = payment
                    expenses[idx] += payment

        # accrue interest on accounts
        for a in accounts:
            if 'intMonthly' in a:  # interest-bearing account
                a['balances'][idx] = compoundInt(a['balances'][idx - 1], a['intMonthly'])

        # add contributions to 401(k), Roth 401(k), and HSA type accounts
        for a in accounts:
            if a['type'] in ['401(k)', 'Roth 401(k)', 'HSA']:
                if ages[idx] >= a['minAge'] and ages[idx] <= a['maxAge']:  # active contributions while working
                  # TODO: add another check for when RMDs kick in (regardless of maxAge)?
                    a['payments'][idx] = a['delMonthly']
                    a['balances'][idx] += a['delMonthly']

        # update end-of-Dec tracking for IRA RMDs
        if idx == nextDecIdx:  # it's Dec, save balances (with new interest) for use next year
            nextDecIdx += 12
            for a in accounts:
                if a['type'] in ['IRA', '401(k)']:
                    a['prevDecBalance'] = a['balances'][idx]

        # determine net cash flow this month
        discret[idx] = incomes[idx] + expenses[idx]
        avail = discret[idx]

        # use positive cash flow against prioritized list of activities
        if avail > 0.0:
            # pay down any outstanding loans
            for a in accounts:
                if a['type'] == 'loan' and a['balances'][idx] < 0.0:
                    # loan with outstanding balance
                    payment = max([-avail, a['balances'][idx]])
                        # max() because balances are negative
                    a['balances'][idx] -= payment
                    a['payments'][idx] = payment
                    avail += payment

                    # notify if loan was just paid off
                    if a['balances'][idx] >= 0.0:
                        print('%s loan paid off at age %0.2f\n' % (a['label'], ages[idx]))

            # maximize Roth IRA contributions
            if avail > 0.0:
                for a in accounts:
                    if a['type'] == 'Roth':
                        # TODO: switch to getRothContrib() with separately calculated earned and Roth
                        # incomes
                        contrib = min([incomes[idx], avail, a['maxContrib']])
                            # can't contribute unless there's earned income to cover it
                        a['balances'][idx] += contrib
                        a['payments'][idx] += contrib
                        avail -= contrib

            # add whatever remains to savings
            if avail > 0.0:
                for a in accounts:
                    if a['type'] == 'savings':
                        a['balances'][idx] += avail
                        a['payments'][idx] += avail
                        avail = 0.0
                        break

        # tap prioritized list of savings to address negative cash flow
        elif avail < 0.0:
            # withdraw from general (taxable) savings
            for a in accounts:
                if a['type'] == 'savings' and a['balances'][idx] > 0.0:
                    # savings with an available balance
                    withdraw = min([-avail, a['balances'][idx]])
                    a['balances'][idx] -= withdraw
                    a['payments'][idx] -= withdraw
                    avail += withdraw  # avail is negative
                # TODO: estimate capital gains realizations

            # withdraw from IRA accounts
            if avail < 0.0:
                for a in accounts:
                    if a['type'] in ['IRA', '401(k)'] and a['balances'][idx] > 0.0:
                        # IRA or 401(k) with an available balance
                        withdraw = min([-avail, a['balances'][idx]])
                        a['balances'][idx] -= withdraw
                        a['payments'][idx] -= withdraw
                        avail += withdraw  # avail is negative
                        incomes[idx] += withdraw
                            # IRA and 401(k) distributions are normal income for tax purposes

            # withdraw from Roth accounts
            if avail < 0.0:
                for a in accounts:
                    if a['type'] in ['Roth', 'Roth 401(k)'] and a['balances'][idx] > 0.0:
                        # Roth with an available balance
                        withdraw = min([-avail, a['balances'][idx]])
                        a['balances'][idx] -= withdraw
                        a['payments'][idx] -= withdraw
                        avail += withdraw  # avail is negative

        # calculate net worth
        for a in accounts:
            if 'balances' in a:
                netWorth[idx] += a['balances'][idx]

    # plot monthly rates
    plotUtils.multiPlot(ages, [incomes, expenses, discret], 'age (yr)', 'rate (2020 $/mo)',
                        ['total income', 'total expenses', 'discretionary'])

    # plot loan class payments and account balances
    balances = []
    payments = []
    names = []
    doPlot = False
    for a in accounts:
        if a['type'] == 'loan':
            doPlot = True
            balances.append(a['balances'])
            payments.append(a['payments'])
            names.append(a['label'])
    if doPlot:
        plotUtils.multiPlot(ages, balances, 'age (yr)', 'balance (2020 $)', names)
        plotUtils.multiPlot(ages, payments, 'age (yr)', 'payments (2020 $/mo)',names)

    # plot savings class account balances
    balances = []
    payments = []
    names = []
    doPlot = False
    for a in accounts:
        if a['type'] in ['savings', '401(k)', 'IRA', 'Roth 401(k)', 'Roth', 'HSA']:
            doPlot = True
            balances.append(a['balances'])
            payments.append(a['payments'])
            names.append(a['label'])
    if doPlot:
        plotUtils.multiPlot(ages, balances, 'age (yr)', 'balance (2020 $)', names)
        plotUtils.multiPlot(ages, payments, 'age (yr)', 'payments (2020 $/mo)', names)

    # plot net worth
    plotUtils.singlePlot(ages, netWorth, 'age (yr)', 'net worth (2020 $)')

    return accounts


def getRothContrib(rothIncome, earnedIncome, maxContrib, phaseOutBeg, phaseOutEnd):
    '''
    Get the allowable Roth IRA contribution according to IRS rules for phase-out and income limits.

    Calculations are based on IRS publication 590-A, Worksheet 2-2 from 2017 (ignoring some minor
    rounding and minimum rules on the final value)
    '''

    if rothIncome < phaseOutBeg:  # contribution limited only by earned income
        contrib = min([earnedIncome, maxContrib])
    elif rothIncome < phaseOutEnd: # contribution limited by phase-out rules
        mult = (phaseOutEnd - rothIncome) /  (phaseOutEnd - phaseOutBeg)
        contrib = mult * min([earnedIncome, maxContrib])
    else:  # ineligible for Roth contributions, income is too high
        contrib = 0.0

    return contrib


def getReqMinDistrib(age, P):
    # TODO: Update based on revised law's increased age
    '''
    Get the required minimum distribution for a 401(k) according to IRS rules. Returned RMDs are
    normalized to monthly amounts.
    - age is the account holder's current age in years
    - P is the account balance/principal as of 31 Dec the previous year

    Calculations are based on IRS publication 590-B, Table III from 2017
    '''

    '''
    Technically, rules allow for first RMD to occur by 1 Apr of the year following the one in which
    the person turns 70.5. This can sometimes forestall when the first distribution must be taken
    for people with birthdays in the first half of the year. The IRS rule wording is a little
    unclear about whether a second withdrawal needs to occur in that same year. The simplifying
    assumption used here is that the first RMD is taken the year the account holder age is 70 and
    proceeds normally on a monthly basis thereafter.
    '''

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
         18.7,
         17.9,
         17.1,
         16.3,
         15.5,
         14.8,
         14.1,
         13.4,
         12.7,
         12.0,
         11.4,
         10.8,
         10.2,
         9.6,
         9.1,
         8.6,
         8.1,
         7.6,
         7.1,
         6.7,
         6.3,
         5.9,
         5.5,
         5.2,
         4.9,
         4.5,
         4.2,
         3.9,
         3.7,
         3.4,
         3.1,
         2.9,
         2.6,
         2.4,
         2.1,
         1.9]  # 115 and over
      # from IRS publication 590-B, Table III, 2017

    # calculate the required minimum distribution
    if age < 70.0:
        RMD = 0.0
    elif age >= 115.0:
        RMD = P / d[-1] / 12.0  # 12: convert annual RMD to a monthly value
    else:
        idx = int(math.floor(age) - 70)
        RMD = P / d[idx] / 12.0

    return RMD