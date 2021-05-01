import numpy as np

params = {}

# ages
params['startAge'] = 39.0 + 11.0 / 12
params['stopAge']  = 100.0
params['birthMonth'] = 5
params['currencyYear'] = '2021'
retirementAge = 60.0

# interest rates
APRInflation = 0.0289  # 1980-2014 US CPI average

# accounts
accounts = [\
{'label'         : 'QSAI salary and bonus',
 'hasIncome'     : True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : (3675.0 * 26.0 + 4455.0) / 12.0,
   # 1H2021 paystub take-home pay with estimated (based on 2020) annual bonus, includes 401(k) and HSA contributions
 'earned'        : True},

{'label'         : 'QSAI retention bonus',
 'hasIncome'     : True,
 'minAge'        : 40.1,
 'maxAge'        : 40.2,
 'delMonthly'    : 39660.0,  # $60,000 paid on ~7/1/2021 after tax withholdings
 'earned'        : True},

{'label'         : 'Social Security (Kirstin)',
 'hasIncome'     : True,
 'minAge'        : 67.0,#62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 1660.5,#396.0,  # 566.0 for age 67, 701.0 for age 70
   # from SSA estimate retrieved in May 2021, based on half of spouse's (at age 67) benefit
 'earned'        : False},

{'label'         : 'Social Security (Sean)',
 'hasIncome'     : True,
 'minAge'        : 70.0,#62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 4160.0,#2284.0,  # 3321.0 for age 67, 4160.0 for age 70
   # from SSA estimate retrieved in May 2021
 'earned'        : False},

{'label'         : 'household budget',
 'hasExpenses'   : True,
 'minAge'        : 0.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : -5000.0},
                    # based on 2020 checking account:
                    # - $48,000 net withdrawals (with savings activity removed)
                    # - 2 x $6,000 Roth IRA contributions

{'label'         : 'taxable savings',
 'hasSavings'    : True,
 'hasBalance'    : True,
 'initBalance'   : 75374.0,
 'intAPR'        : 0.0434 - APRInflation},  # inflation-adjusted returns

{'label'         : 'Roth IRA (Kirstin)',
 'hasBalance'    : True,
 'initBalance'   : 170505.0,
 'intAPR'        : 0.095155 - APRInflation,  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 6000.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contributions
    # based on 2021 rules for married filing jointly

{'label'         : 'Roth IRA (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 589733.0,
 'intAPR'        : 0.069904 - APRInflation,  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 6000.0 / 12,
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contribution
    # based on 2021 rules for married filing jointly

{'label'         : 'Roth 401(k) (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 29070.0,
 'intAPR'        : 0.0711 - APRInflation,  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 19500.0 / 12},

{'label'         : '401(k) (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 6465.0,
 'intAPR'        : 0.0711 - APRInflation,  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 6885.0 / 12,  # 4.5% of 1H2021 salary
 'hasRMDs'       : True},

{'label'         : 'HSA',
 'hasBalance'    : True,
 'initBalance'   : 11454.0,
 'intAPR'        : 0.0531 - APRInflation,  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 7200.0 / 12}
]
