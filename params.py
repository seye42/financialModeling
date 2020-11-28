import numpy as np

params = {}

# ages
params['startAge'] = 39.5833
params['stopAge']  = 90.0
params['birthMonth'] = 5
retirementAge = 60.0

# interest rates
APRInflation = 0.0322  # 1913-2014 US CPI average
APRInvest    = 0.0962  # S&P 25-year annualized (1989-2014)

# accounts
accounts = [\
{'label'         : 'salary',
 'type'          : 'income',
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 4043 * 26.0 / 12.0,
   # Nov 2020 paystub with adjustment to spread Roth 401(k) contributions over full year
 'adjAPR'        : APRInflation},

{'label'         : 'QSAI retention bonus',
 'type'          : 'income',
 'minAge'        : 40.1,
 'maxAge'        : 40.2,
 'delMonthly'    : 45000.0,  # $60,000 paid on ~7/1/2021 after tax withholdings
 'adjAPR'        : 0.0},

{'label'         : 'Social Security (Kirstin)',
 'type'          : 'income',
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 396.0,  # 566.0 for age 67, 701.0 for age 70
   # from SSA estimate retrieved in Nov 2020, DOES NOT INCLUDE BENEFITS FOR SPOUSE (SO VERY CONSERVATIVE ESTIMATE)
 'adjAPR'        : APRInflation},

{'label'         : 'Social Security (Sean)',
 'type'          : 'income',
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 2284.0,  # 3321.0 for age 67, 4160.0 for age 70
   # from SSA estimate retrieved in Nov 2020
 'adjAPR'        : APRInflation},

{'label'         : 'household budget',
 'type'          : 'expense',
 'minAge'        : 0.0,
 'maxAge'        : params['stopAge'],
 'delMonthly'    : -4100.0, # $2700 Citi + $100 REI + $800 property taxes + $500 misc.
 'adjAPR'        : APRInflation},

{'label'         : 'taxable savings',
 'type'          : 'savings',
 'initBalance'   : 60455.0,  # as of startAge
 'intAPR'        : 0.0349 - APRInflation},  # inflation-adjusted returns

{'label'         : 'Roth IRA (Kirstin)',
 'type'          : 'Roth',
 'initBalance'   : 136800.0,
 'intAPR'        : 0.090195 - APRInflation,
 'maxContrib'    : 6000.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBeg'   : np.Inf,  # AGI where phase-out begins
 'phaseOutEnd'   : np.Inf},  # AGI where inelibible for contributions
    # based on 2018 rules for married filing jointly

{'label'         : 'Roth IRA (Sean)',
 'type'          : 'Roth',
 'initBalance'   : 512508.0,
 'intAPR'        : 0.058513 - APRInflation,
 'maxContrib'    : 6000.0 / 12,
 'phaseOutBeg'   : np.Inf,  # AGI where phase-out begins
 'phaseOutEnd'   : np.Inf},  # AGI where inelibible for contribution
    # based on 2018 rules for married filing jointly

{'label'         : 'Roth 401(k) (Sean)',
 'type'          : 'Roth 401(k)',
 'initBalance'   : 15798.0,
 'intAPR'        : 0.0551 - APRInflation,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 19500.0 / 12},

{'label'         : '401(k) (Sean)',
 'type'          : '401(k)',
 'initBalance'   : 2844.0,
 'intAPR'        : 0.0551 - APRInflation,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 6885.0 / 12},  # 4.5% of salary

{'label'         : 'HSA',
 'type'          : 'HSA',
 'initBalance'   : 8914.0,
 'intAPR'        : 0.0491 - APRInflation,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 7200.0 / 12}
]
