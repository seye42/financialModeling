params = {}

# ages
params['startAge'] = 35.0
params['stopAge']  = 75.0

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
 'delMonthly'    : 5500.0,
 'adjAPR'        : 0.0},

{'label'         : 'household budget',
 'type'          : 'expense',
 'delMonthly'    : -2500.0},

{'label'         : 'mortgage',
 'type'          : 'loan',
 'initBalance'   : -61029.0,
 'intAPR'        : 0.03875},

{'label'         : 'taxable savings',
 'type'          : 'savings',
 'initBalance'   : 10.0e3,  # as of startAge
 'intAPR'        : APRInvest - APRInflation},  # inflation-adjusted returns

{'label'         : 'Roth IRA (Kirstin)',
 'type'          : 'Roth',
 'initBalance'   : 71854.0,
 'intAPR'        : 0.1024 - APRInflation,
 'maxContrib'    : 5500.0 / 12},  # annual IRS maximum, normalized to monthly
# TODO: consider if annual basis on this is better strategically (it's certainly much more complicated to handle)

{'label'         : 'Roth IRA (Sean)',
 'type'          : 'Roth',
 'initBalance'   : 90056.0,
 'intAPR'        : 0.0842 - APRInflation,
 'maxContrib'    : 5500.0 / 12},  # annual IRS maximum, normalized to monthly

{'label'         : 'IRA (Kirstin)',
 'type'          : 'IRA',
 'initBalance'   : 13469.0,
 'intAPR'        : 0.0357 - APRInflation},

{'label'         : 'IRA (Sean)',
 'type'          : 'IRA',
 'initBalance'   : 210975.0,
 'intAPR'        : 0.0463 - APRInflation}]  # inflation-adjusted returns

# TODO: may need to add some sense of priority to these things to indicate what
# gets tapped first and what gets filled first (possibly with maximums like a
# Roth)
