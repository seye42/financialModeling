params = {}

# ages
params['startAge'] = 37.0833
params['stopAge']  = 80.0
params['birthMonth'] = 5

# interest rates
APRInflation = 0.0322  # 1913-2014 US CPI average
APRInvest    = 0.0962  # S&P 25-year annualized (1989-2014)

# tax rates

# accounts
accounts = [\
{'label'         : 'salary',
 'type'          : 'income',
 'minAge'        : 0.0,
 'maxAge'        : 65.0,
 'delMonthly'    : 4328.22 * 26.0 / 12.0,  # May 2018 paystub with income taxes added back in
 'adjAPR'        : 0.0},

{'label'         : 'household budget',
 'type'          : 'expense',
 'delMonthly'    : -3500.0}, # $2300 Citi + $300 REI + $700 property taxes + $200 misc.

{'label'         : 'taxable savings',
 'type'          : 'savings',
 'initBalance'   : 4000.0,  # as of startAge
 'intAPR'        : APRInvest - APRInflation},  # inflation-adjusted returns

{'label'         : 'Roth IRA (Kirstin)',
 'type'          : 'Roth',
 'initBalance'   : 88442.83,
 'intAPR'        : 0.1032 - APRInflation,
 'maxContrib'    : 5500.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBeg'   : 189000 / 12,  # AGI where phase-out begins
 'phaseOutEnd'   : 199000 / 12},  # AGE where inelibible for contributions
    # based on 2018 rules for married filing jointly
# TODO: consider if annual basis on this is better strategically (it's certainly much more complicated to handle)

{'label'         : 'Roth IRA (Sean)',
 'type'          : 'Roth',
 'initBalance'   : 109681.92,
 'intAPR'        : 0.0862 - APRInflation,
 'maxContrib'    : 5500.0 / 12,
 'phaseOutBeg'   : 189000 / 12,  # AGI where phase-out begins
 'phaseOutEnd'   : 199000 / 12},  # AGE where inelibible for contributions
    # based on 2018 rules for married filing jointly},  # annual IRS maximum, normalized to monthly

{'label'         : 'IRA (Kirstin)',
 'type'          : 'IRA',
 'initBalance'   : 17415.37,
 'intAPR'        : 0.0357 - APRInflation},

{'label'         : 'IRA (Sean)',
 'type'          : 'IRA',
 'initBalance'   : 268562.81,
 'intAPR'        : 0.0467 - APRInflation}]  # inflation-adjusted returns

# TODO: may need to add some sense of priority to these things to indicate what
# gets tapped first and what gets filled first (possibly with maximums like a
# Roth)
