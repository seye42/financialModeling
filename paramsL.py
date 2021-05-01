params = {}

# ages
params['startAge'] = 11 + 4.0 / 12.0
params['stopAge']  = 22.0
params['birthMonth'] = 12
params['currencyYear'] = '2021'

# interest rates
APRInflation = 0.0289  # 1980-2014 US CPI average
APRInvest    = 0.07258
  # target portfolio construction based on historical per-fund returns retrieved on 12/19/2020

# accounts
accounts = [\
{'label'         : 'tuition & fees',
 'hasExpenses'   : True,
 'minAge'        : 18.75,
 'maxAge'        : 22.75,
 'delMonthly'    : -1265.0},  # average across universities retrieved on 1/1/19

{'label'         : 'household budget',
 'hasExpenses'    : True,
 'minAge'        : 18.75,
 'maxAge'        : 22.75,
 'delMonthly'    : -750.0},

{'label'         : 'UTMA',
 'hasSavings'    : True,
 'hasBalance'    : True,
 'initBalance'   : 119987.0,  # as of startAge
 'intAPR'        : APRInvest - APRInflation}]  # inflation-adjusted returns
