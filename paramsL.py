params = {}

# ages
params['startAge'] = 11
params['stopAge']  = 22
params['birthMonth'] = 12
params['currencyYear'] = '2020'

# interest rates
APRInflation = 0.0322  # 1913-2014 US CPI average
APRInvest    = 0.065025
  # target portfolio construction based on historical per-fund returns retrieved on 11/19/16

# accounts
accounts = [\
{'label'         : 'tuition & fees',
 'hasExpense'    : True,
 'minAge'        : 18.75,
 'maxAge'        : 22.75,
 'delMonthly'    : -1265.0},  # average across universities retrieved on 1/1/19

{'label'         : 'household budget',
 'hasExpense'    : True,
 'minAge'        : 18.75,
 'maxAge'        : 22.75,
 'delMonthly'    : -750.0},

{'label'         : 'UTMA',
 'hasSavings'    : True,
 'hasBalance'    : True,
 'initBalance'   : 104290.0,  # as of startAge
 'intAPR'        : APRInvest - APRInflation}]  # inflation-adjusted returns
