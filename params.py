import numpy as np
import finUtils

params = {}

# ages
params['startAge'] = 40.0 + 7.0 / 12
params['stopAge']  = 100.0
params['birthMonth'] = 5
params['currencyYear'] = '2021'
retirementAge = 60.0

# interest rates
APRInflation = 0.0300  # 1/1980-1/2021 US CPI average

# accounts
accounts = [\
{'label'         : 'QSAI salary and bonus',
 'hasIncome'     : True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : (4200.0 * 26.0 + 5500.0) / 12.0,
   # 2H2021 paystub take-home pay with estimated annual bonus, includes 401(k) and HSA contributions
 'earned'        : True},

{'label'         : 'Social Security (Kirstin)',
 'hasIncome'     : True,
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 1142.5,  # 396.0 for age 62, 566.0 for age 67, 701.0 for age 70
   # from SSA estimate retrieved in May 2021, based on half of spouse's (at age 62) benefit
 'earned'        : False},

{'label'         : 'Social Security (Sean)',
 'hasIncome'     : True,
 'minAge'        : 62.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : 2284.0,  # 2284.0 for age 62, 3321.0 for age 67, 4160.0 for age 70
   # from SSA estimate retrieved in May 2021
 'earned'        : False},

{'label'         : 'household budget',
 'hasExpenses'   : True,
 'minAge'        : 0.0,
 'maxAge'        : np.Inf,
 'delMonthly'    : -5800.0},
   # based on 2021 checking account form Jan to Nov

{'label'         : 'taxable savings',
 'hasSavings'    : True,
 'hasBalance'    : True,
 'initBalance'   : 134989.52,
 'intAPR'        : finUtils.adjustForInflation(0.0469, APRInflation)},  # inflation-adjusted returns

{'label'         : 'Roth IRA (Kirstin)',
 'hasBalance'    : True,
 'initBalance'   : 184229.48,
 'intAPR'        : finUtils.adjustForInflation(0.1035, APRInflation),  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 6000.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contributions
    # based on 2021 rules for married filing jointly

{'label'         : 'Roth IRA (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 626129.01,
 'intAPR'        : finUtils.adjustForInflation(0.0770, APRInflation),  # inflation-adjusted returns
 'hasContributionLimits': True,
 'maxContrib'    : 6000.0 / 12,
 'phaseOutBegAGI': np.Inf,  # AGI where phase-out begins
 'phaseOutEndAGI': np.Inf},  # AGI where inelibible for contribution
    # based on 2021 rules for married filing jointly

{'label'         : 'Roth 401(k) (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 45214.22,
 'intAPR'        : finUtils.adjustForInflation(0.0801, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 19500.0 / 12},

{'label'         : '401(k) (Sean)',
 'hasBalance'    : True,
 'initBalance'   : 11998.70,
 'intAPR'        : finUtils.adjustForInflation(0.0801, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 7097.02 / 12,  # 4.5% of 1H2021 salary
 'hasRMDs'       : True},

{'label'         : 'HSA',
 'hasBalance'    : True,
 'initBalance'   : 16400.42,
 'intAPR'        : finUtils.adjustForInflation(0.0537, APRInflation),  # inflation-adjusted returns
 'hasContributions': True,
 'minAge'        : 0.0,
 'maxAge'        : retirementAge,
 'delMonthly'    : 7200.0 / 12}
]
