import numpy as np
import finUtils

params = {}

# ages
params['startAge'] = 43.0 + 8.0 / 12
params['stopAge']  = 100.0
params['birthMonth'] = 5
params['currencyYear'] = '2025'
retirementAge = 55.0

# interest rates
APRInflation = 0.0309902  # 1980 to 2025 US CPI annualized average
  # from https://www.usinflationcalculator.com/, with i = 3.83 ** (1/44) - 1

# accounts
accounts = [\
{'label'         : 'QSAI salary and bonus',
 'hasIncome'     : True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : (4861.0 * 26.0 + 29745.0) / 12.0,
    # 4Q2024 paystub take-home pay with estimated annual bonus, includes 401(k) and HSA contributions
 'earned'        : True},

{'label'         : 'Social Security (K)',
 'hasIncome'     : True,
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 0.5 * 2722.0,
    # from S SSA estimate retrieved in Jan 2025, based on half of spouse's (at age 62) benefit
 'earned'        : False},

{'label'         : 'Social Security (S)',
 'hasIncome'     : True,
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 2722.0,  # 2722.0 for age 62, 3933.0 for age 67, 4908.0 for age 70
    # from SSA estimate retrieved in Jan 2025
 'earned'        : False},

{'label'         : 'household budget',
 'hasExpenses'   : True,
 'minAge'        : 0.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : -6553.0},
    # based on 2024 annual total expenses +5%, less the ones that are captured elsewhere here

{'label'         : 'taxable savings',
 'hasSavings'    : True,
 'hasBalance'    : True,
 'initBalance'   : 304666.18,
 'intAPR'        : finUtils.adjustForInflation(0.0441, APRInflation)},  # inflation-adjusted returns

{'label'         : 'Roth IRA (K)',
 'hasBalance'    : True,
 'initBalance'   : 206150.32,
 'intAPR'        : finUtils.adjustForInflation(0.0904, APRInflation),  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 7000.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contributions
    # based on 2024 rules for married filing jointly

{'label'         : 'Roth IRA (S)',
 'hasBalance'    : True,
 'initBalance'   : 735938.59,
 'intAPR'        : finUtils.adjustForInflation(0.0793, APRInflation),  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 7000.0 / 12,
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contribution
    # based on 2024 rules for married filing jointly

{'label'         : 'Roth 401(k) (S)',
 'hasBalance'    : True,
 'initBalance'   : 144419.78,
 'intAPR'        : finUtils.adjustForInflation(0.0829, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 23500.0 / 12},  # enough to guarantee match in 401(k) portion

{'label'         : '401(k) (S)',
 'hasBalance'    : True,
 'initBalance'   : 47762.99,
 'intAPR'        : finUtils.adjustForInflation(0.0829, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 8592.55 / 12,  # 4.5% of 4Q2024 salary
 'hasRMDs'       : True},

{'label'         : 'HSA',
 'hasBalance'    : True,
 'initBalance'   : 38495.51,
 'intAPR'        : finUtils.adjustForInflation(0.0437, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 8550.0 / 12},

{'label'         : 'house',
 'hasBalance'    : True,
 'initBalance'   : 505900.0,  # Zillow estimate from Jan 2025 for recent Devonshire floorplans
 'intAPR'        : 0.00825,  # inflation-adjusted returns
    # based on Farrand's purchase price of $206,145 on 4/16/1997, the Zillow estimate above, and inflation over the
    # intervening period from https://www.usinflationcalculator.com/
 'hasContributions': False,
 'minAge'        : 0.0,
 'maxAge'        : np.inf,
 'delMonthly'    : 0.0}
]