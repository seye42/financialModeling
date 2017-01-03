import math
import numpy as np
import matplotlib.pyplot as plt



def convAPRtoMon(rAnnual):
    """
    Convert APR to equivalent monthly rate
    """

    # solve (1 + rAnnual) = (1 + rMonthly) ** 12
    rMonthly = (1.0 + rAnnual) ** (1.0 / 12.0) - 1.0

    return rMonthly



def getReqMinDistrib(age, P):
    """
    Get the required minimum distribution for a 401(k) according to IRS rules.
    Returned RMDs are normalized to monthly amounts.
    - age is the account holder's current age in years
    - P is the account balance/principal as of 31 Dec the previous year

    Calculations are based on IRS publication 590-B, Table III from 2015
    """

    # Technically, rules allow for first RMD to occur by 1 Apr of the year
    # following the one in which the person turns 70.5.  This can sometimes
    # forestall when the first distribution must be taken for people with
    # birthdays in the first half of the year.  The IRS rule wording is a
    # little unclear about whether a second withdrawal needs to occur in that
    # same year.  Simplifying assumption here is that the first RMD is taken
    # the year the account holder age is 70 and proceeds normally on a monthly
    # basis thereafter.

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
      # from IRS publication 590-B, Table III, 2015

    # calculate the required minimum distribution
    if age < 70.0:
        RMD = 0.0
    elif age >= 115.0:
        RMD = P / d[-1] / 12.0  # 12: convert annual RMD to a monthly value
    else:
        idx = int(math.floor(age) - 70)
        RMD = P / d[idx] / 12.0

    return RMD



def timeSeries(params, accounts):
    # build age array
    ages = np.arange(params["startAge"], params["stopAge"], 1.0 / 12)
        # in years, but always with monthly steps

    # initialize aggregate time series arrays
    incomes  = np.zeros_like(ages)
    expenses = np.zeros_like(ages)
    discret  = np.zeros_like(ages)
    netWorth = np.zeros_like(ages)

    # initialize interest-bearing accounts
    for a in accounts:
        if "intAPR" in a:
            # convert APR to monthly rate
            a["intMonthly"] = convAPRtoMon(a["intAPR"])

            # initialize balance time series
            a["balances"] = np.zeros_like(ages)
            a["balances"][0] = a["initBalance"]
            netWorth[0] += a["initBalance"]
        if a["type"] == "loan":
            a["payments"] = np.zeros_like(ages)

    # run time series calculations
    for idx in range(1, len(ages)):  # skip the first age since it's just initial value data
        # get total income and expenses for this period
        for a in accounts:
            if a["type"] == "income":
                incomes[idx] += a["delMonthly"]
            elif a["type"] == "expense":
                expenses[idx] += a["delMonthly"]

        # accrue interest on accounts
        for a in accounts:
            if "intMonthly" in a:
                a["balances"][idx] = a["balances"][idx - 1] * (1.0 + a["intMonthly"])

        # determine net cash flow this month
        discret[idx] = incomes[idx] + expenses[idx]
        avail = discret[idx]

        # pay down any outstanding loans
        if avail > 0.0:
            for a in accounts:
                if a["type"] == "loan" and a["balances"][idx] < 0.0:
                    # loan with outstanding balance
                    payment = max([-avail, a["balances"][idx]])  # max() because balances are negative
                    a["balances"][idx] -= payment
                    a["payments"][idx] = payment
                    avail += payment

                    # notify if loan was just paid off
                    if a["balances"][idx] >= 0.0:
                        print("%s loan paid off at age %0.2f\n" % (a["label"], ages[idx]))

        # maximize Roth IRA contributions
        if avail > 0.0:
            for a in accounts:
                if a["type"] == "Roth":
                    contrib = min([incomes[idx], avail, a["maxContrib"]])
                        # can't contribute unless there's earned income to cover it
                    a["balances"][idx] += contrib
                    avail -= contrib

        # add whatever remains to savings
        if avail > 0.0:
            for a in accounts:
                if a["type"] == "savings":
                    a["balances"][idx] += avail
                    avail = 0.0

        # CORE ASSUMPTION HERE is that the discretionary money use prioritization is
        # monthly expenses, then loans, then Roths, then taxable savings
        # TODO: revisit this

        # calculate net worth
        for a in accounts:
            if "balances" in a:
                netWorth[idx] += a["balances"][idx]

    # plot monthly rates
    plt.figure()
    plt.plot(ages, incomes, 'r', ages, expenses, 'g', ages, discret, 'b')
    plt.xlabel("age (yr)")
    plt.ylabel("rate (2016 $/mo)")
    plt.legend(["total income", "total expenses", "discretionary"], loc="best")

    # plot loan class payments and account balances
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.hold(True)
    labels = []
    for a in accounts:
        if a["type"] == "loan":
            plt.plot(ages, a["balances"])
            labels.append(a["label"])
    plt.xlabel("age (yr)")
    plt.ylabel("balance (2016 $)")
    plt.legend(labels, loc="best")
    plt.subplot(2, 1, 2)
    plt.hold(True)
    for a in accounts:
        if a["type"] == "loan":
            plt.plot(ages, a["payments"])
    plt.xlabel("age (yr)")
    plt.ylabel("payment (2016 $/mo)")
    plt.legend(labels, loc="best")

    # plot savings class account balances
    plt.figure()
    plt.hold(True)
    labels = []
    for a in accounts:
        if a["type"] in ["savings", "Roth", "IRA"]:
            plt.plot(ages, a["balances"])
            labels.append(a["label"])
    plt.xlabel("age (yr)")
    plt.ylabel("balance (2016 $)")
    plt.legend(labels, loc="best")

    # plot net worth
    plt.figure()
    plt.plot(ages, netWorth / 1.0e6, 'r')
    plt.xlabel("age (yr)")
    plt.ylabel("net worth (2016 $M)")

    return accounts
