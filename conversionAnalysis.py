import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def calculateFederalTaxes(income):

    # based on 2019 single tax brackets
    tax = 0.0
    if income > 0.0 and income <= 9700.0:
        tax = 0.0 + 0.1 * (income - 0.0)
    elif income > 9700.0 and income <= 39475.0:
        tax = 970.0 + 0.12 * (income - 9700.0)
    elif income > 39475.0 and income <= 84200.0:
        tax = 4543.0 + 0.22 * (income - 39475.0)
    elif income > 84200.0 and income <= 160725.0:
        tax = 14382.5 + 0.24 * (income - 84200.0)
    elif income > 160725.0 and income <= 204100.0:
        tax = 32748.5 + 0.32 * (income - 160725.0)
    elif income > 204100.0 and income <= 510300.0:
        tax = 46628.5 + 0.35 * (income - 204100.0)
    elif income > 510300.0:
        tax = 153798.5 + 0.37 * (income - 510300.0)

    return tax


def calculateSSIRMAAs(income):

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


# parameters
baseIncome = 36000.0 + 0.85 * 31987.2 + 4000.0
  # Delta + SS + taxable savings dividends for the entire year
convIncome = np.arange(0.0, 300932.0, 64.0)  # max is total IRA balance
stateTaxRate = 0.0425

# calculate the base tax, additional tax, and IRMAA penalties at each conversion value
baseTax = calculateFederalTaxes(baseIncome) + stateTaxRate * baseIncome
convTax = np.empty_like(convIncome)
IRMAAPen = np.empty_like(convIncome)
for i in xrange(convIncome.size):
    convTax[i] = calculateFederalTaxes(baseIncome + convIncome[i]) + \
                 stateTaxRate * (baseIncome + convIncome[i]) - baseTax
    IRMAAPen[i] = calculateSSIRMAAs(baseIncome + convIncome[i])
totalCost = convTax + IRMAAPen
convEfficiency = totalCost / convIncome

# plot
matplotlib.rcParams.update({'font.size': 20, 'figure.facecolor': 'w', 'lines.linewidth': 2})

plt.figure()
plt.plot(convIncome / 1000.0, convTax / 1000.0)
plt.xlabel('converted balance ($k)')
plt.ylabel('additional income tax ($k)')
plt.grid()

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
plt.plot(convIncome / 1000.0, totalCost / convIncome)
plt.xlabel('converted balance ($k)')
plt.ylabel('cost per dollar converted')
plt.grid()