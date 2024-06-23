import numpy as np
import finUtils

params = {}

# ages
params['startAge'] = 43.0 + 1.0 / 12
params['stopAge']  = 100.0
params['birthMonth'] = 5
params['currencyYear'] = '2024'
retirementAge = 60.0

# interest rates
APRInflation = 0.0308675  # 1980 to 2024 US CPI annualized average
  # from https://www.usinflationcalculator.com/, with i = 3.81 ** (1/44) - 1

# accounts
accounts = [\
{'label'         : 'QSAI salary and bonus',
 'hasIncome'     : True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : (4456.0 * 26.0 + 35000.0) / 12.0,
    # 2Q2024 paystub take-home pay with estimated annual bonus, includes 401(k) and HSA contributions
 'earned'        : True},

{'label'         : 'Social Security (K)',
 'hasIncome'     : True,
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 1320.5,
    # from S SSA estimate retrieved in Jun 2024, based on half of spouse's (at age 62) benefit
 'earned'        : False},

{'label'         : 'Social Security (S)',
 'hasIncome'     : True,
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 2641.0,  # 2641.0 for age 62, 3827.0 for age 67, 4785.0 for age 70
    # from SSA estimate retrieved in Jun 2024
 'earned'        : False},

{'label'         : 'household budget',
 'hasExpenses'   : True,
 'minAge'        : 0.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : -6265.0},
    # based on 2023 annual total expenses +5%, less the ones that are captured elsewhere here

{'label'         : 'taxable savings',
 'hasSavings'    : True,
 'hasBalance'    : True,
 'initBalance'   : 270070.7,
 'intAPR'        : finUtils.adjustForInflation(0.0431, APRInflation)},  # inflation-adjusted returns

{'label'         : 'Roth IRA (K)',
 'hasBalance'    : True,
 'initBalance'   : 187079.39,
 'intAPR'        : finUtils.adjustForInflation(0.0892, APRInflation),  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 7000.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contributions
    # based on 2024 rules for married filing jointly

{'label'         : 'Roth IRA (S)',
 'hasBalance'    : True,
 'initBalance'   : 681385.89,
 'intAPR'        : finUtils.adjustForInflation(0.0724, APRInflation),  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 7000.0 / 12,
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contribution
    # based on 2024 rules for married filing jointly

{'label'         : 'Roth 401(k) (S)',
 'hasBalance'    : True,
 'initBalance'   : 121105.03,
 'intAPR'        : finUtils.adjustForInflation(0.0743, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 23000.0 / 12},  # enough to guarantee match in 401(k) portion

{'label'         : '401(k) (S)',
 'hasBalance'    : True,
 'initBalance'   : 39665.75,
 'intAPR'        : finUtils.adjustForInflation(0.0743, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 8326.12 / 12,  # 4.5% of 2Q2024 salary
 'hasRMDs'       : True},

{'label'         : 'HSA',
 'hasBalance'    : True,
 'initBalance'   : 33564.39,
 'intAPR'        : finUtils.adjustForInflation(0.0450, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 8300.0 / 12},

{'label'         : 'house',
 'hasBalance'    : True,
 'initBalance'   : 526200.0,  # Zillow estimate from 6/22/2024 for recent Devonshire floorplans
 'intAPR'        : 0.00989,  # inflation-adjusted returns
    # based on Farrand's purchase price of $206,145 on 4/16/1997, the Zillow estimate above, and inflation over the
    # intervening period from https://www.usinflationcalculator.com/
 'hasContributions': False,
 'minAge'        : 0.0,
 'maxAge'        : np.inf,
 'delMonthly'    : 0.0}
]