params = {}

# ages
params['startAge'] = 9
params['stopAge']  = 22
params['birthMonth'] = 12

# interest rates
APRInflation = 0.0322  # 1913-2014 US CPI average
APRInvest    = 0.065025
  # target portfolio construction based on historical per-fund returns retrieved on 11/19/16

# accounts
accounts = [\
{'label'         : 'tuition & fees',
 'type'          : 'expense',
 'minAge'        : 18.75,
 'maxAge'        : 22.75,
 'delMonthly'    : -1265.0,  # average across universities retrieved on 1/1/19
 'adjAPR'        : APRInflation},

{'label'         : 'household budget',
 'type'          : 'expense',
 'minAge'        : 18.75,
 'maxAge'        : 22.75,
 'delMonthly'    : -750.0,  # average across universities retrieved on 1/1/19
 'adjAPR'        : APRInflation},

{'label'         : 'UTMA',
 'type'          : 'savings',
 'initBalance'   : 67125.0,  # as of startAge
 'intAPR'        : APRInvest - APRInflation}]  # inflation-adjusted returns
