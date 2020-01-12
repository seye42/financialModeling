import numpy as np

params = {}

# ages
params['startAge'] = 38.6667
params['stopAge']  = 90.0
params['birthMonth'] = 5

# interest rates
APRInflation = 0.0322  # 1913-2014 US CPI average
APRInvest    = 0.0962  # S&P 25-year annualized (1989-2014)

# tax rates

# accounts
accounts = [\
{'label'         : 'salary',
 'type'          : 'income',
 'minAge'        : 0.0,
 'maxAge'        : 64.0,
 'delMonthly'    : 4341 * 26.0 / 12.0,  # May 2018 paystub with income taxes added back in
 'adjAPR'        : APRInflation},

{'label'         : 'household budget',
 'type'          : 'expense',
 'minAge'        : 0.0,
 'maxAge'        : params['stopAge'],
 'delMonthly'    : -4000.0, # $2700 Citi + $100 REI + $800 property taxes + $400 misc.
 'adjAPR'        : APRInflation},

{'label'         : 'taxable savings',
 'type'          : 'savings',
 'initBalance'   : 10106.86,  # as of startAge
 'intAPR'        : 0.0551 - APRInflation},  # inflation-adjusted returns

{'label'         : 'Roth IRA (Kirstin)',
 'type'          : 'Roth',
 'initBalance'   : 127342.66,
 'intAPR'        : 0.08933 - APRInflation,
 'maxContrib'    : 6000.0 / 12,  # annual IRS maximum, normalized to monthly
 'phaseOutBeg'   : np.Inf,  # AGI where phase-out begins
 'phaseOutEnd'   : np.Inf},  # AGI where inelibible for contributions
    # based on 2018 rules for married filing jointly
# TODO: consider if annual basis on this is better strategically (it's certainly much more complicated to handle)

{'label'         : 'Roth IRA (Sean)',
 'type'          : 'Roth',
 'initBalance'   : 440480.36,
 'intAPR'        : 0.05487 - APRInflation,
 'maxContrib'    : 6000.0 / 12,
 'phaseOutBeg'   : np.Inf,  # AGI where phase-out begins
 'phaseOutEnd'   : np.Inf},  # AGI where inelibible for contribution
    # based on 2018 rules for married filing jointly

{'label'         : 'HSA',
 'type'          : 'Roth',  # TODO: Add HSA (non-taxed savings)
 'initBalance'   : 2453.45,
 'intAPR'        : 0.0491 - APRInflation,
 'maxContrib'    : 0.0,
 'phaseOutBeg'   : 0.0,  # AGI where phase-out begins
 'phaseOutEnd'   : 0.0}]  # AGI where inelibible for contributions

# TODO: may need to add some sense of priority to these things to indicate what
# gets tapped first and what gets filled first (possibly with maximums like a
# Roth)
