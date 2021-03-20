import numpy as np

params = {}

# ages
params['startAge'] = 39.0 + 7.0 / 12
params['stopAge']  = 100.0
params['birthMonth'] = 5
params['currencyYear'] = '2020'
retirementAge = 60.0

# interest rates
APRInflation = 0.0322  # 1913-2014 US CPI average
APRInvest    = 0.0962  # S&P 25-year annualized (1989-2014)

# accounts
accounts = [\
{'label'         : 'QSAI salary and bonus',
 'hasIncome'     : True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : (4043 * 26.0 + 4500.0) / 12.0,
   # Nov 2020 paystub with estimated annual bonus and adjustment to spread Roth 401(k) contributions over full year
 'earned'        : True},

{'label'         : 'QSAI retention bonus',
 'hasIncome'     : True,
 'minAge'        : 40.1,
 'maxAge'        : 40.2,
 'delMonthly'    : 45000.0,  # $60,000 paid on ~7/1/2021 after tax withholdings
 'earned'        : True},

{'label'         : 'Social Security (Kirstin)',
 'hasIncome'     : True,
 'minAge'        : 70.0,#62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 701.0,#396.0,  # 566.0 for age 67, 701.0 for age 70
   # from SSA estimate retrieved in Nov 2020, DOES NOT INCLUDE BENEFITS FOR SPOUSE (SO VERY CONSERVATIVE ESTIMATE)
 'earned'        : False},

{'label'         : 'Social Security (Sean)',
 'hasIncome'     : True,
 'minAge'        : 70.0,#62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 4160.0,#2284.0,  # 3321.0 for age 67, 4160.0 for age 70
   # from SSA estimate retrieved in Nov 2020
 'earned'        : False},

{'label'         : 'household budget',
 'hasExpenses'   : True,
 'minAge'        : 0.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : -4100.0}, # $2700 Citi + $100 REI + $800 property taxes + $500 misc.

{'label'         : 'taxable savings',
 'hasSavings'    : True,
 'hasBalance'    : True,
 'initBalance'   : 60455.0,  # as of startAge
 'intAPR'        : 0.0434 - APRInflation},  # inflation-adjusted returns

{'label'         : 'Roth IRA (Kirstin)',
 'hasBalance'    : True,
 'initBalance'   : 136800.0,
 'intAPR'        : 0.095162 - APRInflation,  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 6000.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contributions
    # based on 2018 rules for married filing jointly

{'label'         : 'Roth IRA (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 512508.0,
 'intAPR'        : 0.0703522 - APRInflation,  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 6000.0 / 12,
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contribution
    # based on 2018 rules for married filing jointly

{'label'         : 'Roth 401(k) (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 15798.0,
 'intAPR'        : 0.0711 - APRInflation,  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 19500.0 / 12},

{'label'         : '401(k) (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 2844.0,
 'intAPR'        : 0.0711 - APRInflation,  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 6885.0 / 12,  # 4.5% of salary
 'hasRMDs'       : True},

{'label'         : 'HSA',
 'hasBalance'    : True,
 'initBalance'   : 8914.0,
 'intAPR'        : 0.0531 - APRInflation,  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 7200.0 / 12}
]
