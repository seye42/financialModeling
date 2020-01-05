import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import fedIncomeTax


def calculateSSIRMAAs2019S(income):

    # based on 2019 single tax brackets
    IRMAA = 0.0
    if income > 85000.0 and income <= 107000.0:
        IRMAA = 12.0 * (54.1 + 12.4)
    elif income > 107000.0 and income <= 133500.0:
        IRMAA = 12.0 * (135.4 + 31.9)
    elif income > 133500.0 and income <= 160000.0:
        IRMAA = 12.0 * (216.7 + 51.4)
    elif income > 160000.0 and income <= 499999.99:
        IRMAA = 12.0 * (297.9 + 70.9)
    elif income > 499999.99:
        IRMAA = 12.0 * (325.0 + 77.4)

    return IRMAA


def calculateSSIRMAAs2020S(income):

    # based on 2019 single tax brackets
    IRMAA = 0.0
    if income > 87000.0 and income <= 109000.0:
        IRMAA = 12.0 * (202.4 - 144.6 + 12.2)
    elif income > 109000.0 and income <= 136000.0:
        IRMAA = 12.0 * (289.2 - 144.6 + 31.5)
    elif income > 136000.0 and income <= 163000.0:
        IRMAA = 12.0 * (376.0 - 144.6 + 50.7)
    elif income > 163000.0 and income <= 499999.99:
        IRMAA = 12.0 * (462.7 - 144.6 + 70.0)
    elif income > 499999.99:
        IRMAA = 12.0 * (491.6 - 144.6 + 76.4)

    return IRMAA


def noSSIRMAA(income):
    return 0.0


# parameters
setID = 3
stateTaxRate = 0.0425
if setID == 0:
    # KS: 2019
    baseIncome = 5500.0 + 75430.74 + 13840.43 + (12.0 / 26.0) * 151e3 + 2539.91
      # 2018 bonus + QS ~1/2 salary + QS PTO payout + QSAI ~1/2 salary + capital gains and dividends (as of 12/13/19)
    federalDeduction = 24400.0
    stateExemption = 4 * 4400.0
    maxConversion = 270e3
    fedBracket = fedIncomeTax.brackets2019MFJ
    funcSSIRMAA = noSSIRMAA
elif setID == 1:
    # L: 2019
    baseIncome = 36e3 + 0.85 * 31987.2 + 4e3
      # Delta + SS + taxable savings dividends for the entire year
    federalDeduction = 12200.0
    stateExemption = 4400.0
    maxConversion = 301e3
    fedBracket = fedIncomeTax.brackets2019S
    funcSSIRMAA = calculateSSIRMAAs2019S
elif setID == 2:
    # KS: 2020
    baseIncome = 0.5 * 151e3 + 1.05 * 0.5 * 151e3 + 8e3 + 60e3 + 2e3
      # 1H20 salary + 2H20 salary (with 5% raise) + annual bonus + retention bonus + estimated capital gains and dividends
    federalDeduction = 24800.0
    stateExemption = 4 * 4750.0
    maxConversion = 140000.0
    fedBracket = fedIncomeTax.brackets2020MFJ
    funcSSIRMAA = noSSIRMAA
elif setID == 3:
    # L: 2020
    baseIncome = 36e3 + 0.85 * 31987.2 + 4e3
      # Delta + SS + taxable savings dividends for the entire year
      # TODO: Update SS and savings components
    federalDeduction = 12400.0
    stateExemption = 4750.0
    maxConversion = 250e3
    fedBracket = fedIncomeTax.brackets2020S
    funcSSIRMAA = calculateSSIRMAAs2020S


# calculate the base tax, additional tax, and IRMAA penalties at each conversion value
convIncome = np.arange(0.01, maxConversion, 64.0)
baseTax = fedIncomeTax.calculateTax(fedBracket, baseIncome - federalDeduction) + stateTaxRate * (baseIncome - stateExemption)
convTax = np.empty_like(convIncome)
IRMAAPen = np.empty_like(convIncome)
for i in range(convIncome.size):
    convTax[i] = fedIncomeTax.calculateTax(fedBracket, baseIncome + convIncome[i] - federalDeduction) + \
                 stateTaxRate * (baseIncome + convIncome[i] - stateExemption) - baseTax
      # income taxes are based on AGI once reduced by the federal deduction and state exemption
    IRMAAPen[i] = funcSSIRMAA(baseIncome + convIncome[i])
      # IRMAA penalties are based on AGI directly (no adjustment for federal deductions)
totalCost = convTax + IRMAAPen
convEfficiency = totalCost / convIncome

# plot
matplotlib.rcParams.update({'font.size': 20, 'figure.facecolor': 'w', 'lines.linewidth': 2})

plt.figure()
plt.plot(convIncome / 1000.0, convTax / 1000.0)
plt.xlabel('converted balance ($k)')
plt.ylabel('additional income tax ($k)')
plt.grid()

if funcSSIRMAA is not noSSIRMAA:
    plt.figure()
    plt.plot(convIncome / 1000.0, IRMAAPen / 1000.0)
    plt.xlabel('converted balance ($k)')
    plt.ylabel('annual IRMAA penalties ($k)')
    plt.grid()

    plt.figure()
    plt.plot(convIncome / 1000.0, totalCost / 1000.0)
    plt.xlabel('converted balance ($k)')
    plt.ylabel('total additional cost ($k)')
    plt.grid()

plt.figure()
plt.plot(convIncome / 1000.0, convEfficiency)
plt.xlabel('converted balance ($k)')
plt.ylabel('cost per dollar converted')
plt.grid()