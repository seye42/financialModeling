import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import fedIncomeTax


def calculateSSIRMAAs2019S(income):

    # based on 2020 single status, combined Part B and Part D IRMAA costs above the standard premium amount
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

    # based on 2020 single status, combined Part B and Part D IRMAA costs above the standard premium amount
    IRMAA = 0.0
    if income > 87000.0 and income <= 109000.0:
        IRMAA = 12.0 * (202.4 - 144.6 + 12.2)
    elif income > 109000.0 and income <= 136000.0:
        IRMAA = 12.0 * (289.2 - 144.6 + 31.5)
    elif income > 136000.0 and income <= 163000.0:
        IRMAA = 12.0 * (376.0 - 144.6 + 50.7)
    elif income > 163000.0 and income < 500000.0:
        IRMAA = 12.0 * (462.7 - 144.6 + 70.0)
    elif income >= 500000.0:
        IRMAA = 12.0 * (491.6 - 144.6 + 76.4)

    return IRMAA


def calculateSSIRMAAs2020MFJ(income):

    # based on 2020 married filing jointly status, combined Part B and Part D IRMAA costs above the standard premium
    # amount
    IRMAA = 0.0
    if income > 174000.0 and income <= 218000.0:
        IRMAA = 12.0 * (202.4 - 144.6 + 12.2)
    elif income > 218000.0 and income <= 272000.0:
        IRMAA = 12.0 * (289.2 - 144.6 + 31.5)
    elif income > 272000.0 and income <= 326000.0:
        IRMAA = 12.0 * (376.0 - 144.6 + 50.7)
    elif income > 326000.0 and income < 750000.0:
        IRMAA = 12.0 * (462.7 - 144.6 + 70.0)
    elif income >= 750000.0:
        IRMAA = 12.0 * (491.6 - 144.6 + 76.4)

    return IRMAA


def calculateSSIRMAAs2021S(income):

    # based on 2021 single status, combined Part B and Part D IRMAA costs above the standard premium amount
    IRMAA = 0.0
    if income > 88000.0 and income <= 111000.0:
        IRMAA = 12.0 * (207.9 - 148.6 + 12.3)
    elif income > 111000.0 and income <= 138000.0:
        IRMAA = 12.0 * (297.0 - 148.6 + 31.8)
    elif income > 138000.0 and income <= 165000.0:
        IRMAA = 12.0 * (386.1 - 148.6 + 51.2)
    elif income > 165000.0 and income < 500000.0:
        IRMAA = 12.0 * (475.2 - 148.6 + 70.7)
    elif income >= 500000.0:
        IRMAA = 12.0 * (504.9 - 148.6 + 77.10)

    return IRMAA


def calculateSSIRMAAs2021MFJ(income):

    # based on 2021 married filing jointly status, combined Part B and Part D IRMAA costs above the standard premium
    # amount
    IRMAA = 0.0
    if income > 176000.0 and income <= 222000.0:
        IRMAA = 12.0 * (207.9 - 148.6 + 12.3)
    elif income > 222000.0 and income <= 276000.0:
        IRMAA = 12.0 * (297.0 - 148.6 + 31.8)
    elif income > 276000.0 and income <= 330000.0:
        IRMAA = 12.0 * (386.1 - 148.6 + 51.2)
    elif income > 330000.0 and income < 750000.0:
        IRMAA = 12.0 * (475.2 - 148.6 + 70.7)
    elif income >= 750000.0:
        IRMAA = 12.0 * (504.9 - 148.6 + 77.10)

    return IRMAA


def noSSIRMAA(income):
    return 0.0


def calculateMIIncomeTax(income):
    return 0.0425 * income


def calculateKSIncomeTax2020MFJ(income):

    # based on 2020 Kansas resident, married, joint status
    if income <= 30000.0:
        tax = 0.031 * income
    elif income > 30000.0 and income <= 60000.0:
        tax =  930.0 + 0.0525 * (income - 30000.0)
    elif income > 60000.0:
        tax = 2505.0 + 0.057 * (income - 60000.0)

    return tax


calculateKSIncomeTax2021MFJ = calculateKSIncomeTax2020MFJ

# parameters
setID = 6
if setID == 0:
    # KS: 2019
    baseIncome = 5500.0 + 75430.74 + 13840.43 + (12.0 / 26.0) * 151e3 + 2539.91
      # 2018 bonus + QS ~1/2 salary + QS PTO payout + QSAI ~1/2 salary + capital gains and dividends (as of 12/13/19)
    federalDeduction = 24400.0
    stateExemption = 4 * 4400.0
    stateModification = 0.0
    maxConversion = 270e3
    fedBracket = fedIncomeTax.brackets2019MFJ
    funcState = calculateMIIncomeTax
    funcSSIRMAA = noSSIRMAA
    scaleSSIRMAA = 0.0
elif setID == 1:
    # L: 2019
    baseIncome = 36e3 + 0.85 * 31987.2 + 4e3
      # Delta + SS + taxable savings dividends for the entire year
    federalDeduction = 12200.0
    stateExemption = 4400.0
    stateModification = 0.0
    maxConversion = 301e3
    fedBracket = fedIncomeTax.brackets2019S
    funcState = calculateMIIncomeTax
    funcSSIRMAA = calculateSSIRMAAs2019S
    scaleSSIRMAA = 1.0
elif setID == 2:
    # KS: 2020
    baseIncome = 0.5 * 151e3 + 1.03 * 0.5 * 151e3 + 8e3 + 60e3 + 1500.0
      # 1H20 salary + 2H20 salary (with 3% raise) + annual bonus + retention bonus + estimated capital gains and dividends
    federalDeduction = 24800.0
    stateExemption = 4 * 4750.0
    stateModification = 0.0
    maxConversion = 139287.14
    fedBracket = fedIncomeTax.brackets2020MFJ
    funcState = calculateMIIncomeTax
    funcSSIRMAA = noSSIRMAA
    scaleSSIRMAA = 0.0
elif setID == 3:
    # L: 2020
    baseIncome = 36e3 + 0.85 * 32496.0 + 4.2e3
      # Delta + SS + taxable savings dividends for the entire year
      # TODO: Update SS and savings components
    federalDeduction = 12400.0
    stateExemption = 4750.0
    stateModification = 0.0
    maxConversion = 252762.57
    fedBracket = fedIncomeTax.brackets2020S
    funcState = calculateMIIncomeTax
    funcSSIRMAA = calculateSSIRMAAs2020S
    scaleSSIRMAA = 1.0
elif setID == 4:
    # CS: 2020
    baseIncome = 79010.0 + 22960.0 + 52.0  # both salaries and interest earnings
    federalDeduction = 24800.0 + 1300.0  # standard MFJ with one "over 65 or blind" adjustment
    stateExemption = 2250.0 * 2 + 8200.0  # 2 exemptions plus standard MFJ deduction with one "over 65" adjustment
    stateModification = 5223.0  # KPERS contributions that are included in K-40 income modifications
    maxConversion = 100000.0
    fedBracket = fedIncomeTax.brackets2020MFJ
    funcState = calculateKSIncomeTax2020MFJ
    funcSSIRMAA = calculateSSIRMAAs2020MFJ
    scaleSSIRMAA = 1.0 + 0.75
      # full year for C, but only 2Q-4Q of 2022 for S
elif setID == 5:
    # L: 2021
    baseIncome = 36e3 + 0.85 * 32496.0 + 4.2e3
      # Delta + SS + taxable savings dividends for the entire year
      # TODO: Update SS and savings components
    federalDeduction = 12550.0
    stateExemption = 4750.0
    stateModification = 0.0
    maxConversion = 135000.0
    fedBracket = fedIncomeTax.brackets2021S
    funcState = calculateMIIncomeTax
    funcSSIRMAA = calculateSSIRMAAs2021S
    scaleSSIRMAA = 1.0
elif setID == 6:
    # CS: 2021
    baseIncome = 79010.0 + 5.0 / 12.0 * 22960.0 + 52.0  # both salaries and interest earnings
    federalDeduction = 25100.0 + 1300.0  # standard MFJ with one "over 65 or blind" adjustment
    stateExemption = 2250.0 * 2 + 8200.0  # 2 exemptions plus standard MFJ deduction with one "over 65" adjustment
    stateModification = 5223.0  # KPERS contributions that are included in K-40 income modifications
    maxConversion = 100000.0
    fedBracket = fedIncomeTax.brackets2021MFJ
    funcState = calculateKSIncomeTax2021MFJ
    funcSSIRMAA = calculateSSIRMAAs2021MFJ
    scaleSSIRMAA = 2.0

# calculate the base tax, additional tax, and IRMAA penalties at each conversion value
convIncome = np.linspace(0.01, maxConversion, 1024)
baseState = funcState(baseIncome + stateModification - stateExemption)
baseFed = fedIncomeTax.calculateTax(fedBracket, baseIncome - federalDeduction)
stateTax = np.empty_like(convIncome)
fedTax   = np.empty_like(convIncome)
IRMAAPen = np.empty_like(convIncome)
for i in range(convIncome.size):
    stateTax[i] = funcState(baseIncome + stateModification + convIncome[i] - stateExemption) - baseState
    fedTax[i] = fedIncomeTax.calculateTax(fedBracket, baseIncome + convIncome[i] - federalDeduction) - baseFed
      # income taxes are based on AGI once reduced by the federal deduction and state exemption
    IRMAAPen[i] = scaleSSIRMAA * funcSSIRMAA(baseIncome + convIncome[i])
      # IRMAA penalties are based on AGI directly (no adjustment for federal deductions)
convTax = stateTax + fedTax
totalCost = convTax + IRMAAPen
convEfficiency = totalCost / convIncome

# plot
matplotlib.rcParams.update({'font.size': 20, 'figure.facecolor': 'w', 'lines.linewidth': 2})

plt.figure()
plt.plot(convIncome / 1000.0, stateTax / 1000.0, label='state')
plt.plot(convIncome / 1000.0, fedTax   / 1000.0, label='federal')
plt.plot(convIncome / 1000.0, convTax  / 1000.0, label='total')
plt.xlabel('converted balance ($k)')
plt.ylabel('additional income tax ($k)')
plt.legend()
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