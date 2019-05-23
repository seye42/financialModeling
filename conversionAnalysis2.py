import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def calculateFederalTaxes(income):

    # based on 2019 MFJ tax brackets
    tax = 0.0
    if income > 0.0 and income <= 19050.0:
        tax = 0.0 + 0.1 * (income - 0.0)
    elif income > 19050.0 and income <= 77400.0:
        tax = 1905.0 + 0.12 * (income - 19050.0)
    elif income > 77400.0 and income <= 165000.0:
        tax = 8907.0 + 0.22 * (income - 77400.0)
    elif income > 165000.0 and income <= 315000.0:
        tax = 28179.0 + 0.24 * (income - 165000.0)
    elif income > 315000.0 and income <= 400000.0:
        tax = 64179.0 + 0.32 * (income - 315000.0)
    elif income > 400000.0 and income <= 600000.0:
        tax = 91379.0 + 0.35 * (income - 400000.0)
    elif income > 600000.0:
        tax = 161379.0 + 0.37 * (income - 600000.0)

    return tax


# parameters
baseIncome = 5500.0 + 0.5 * 140085.55 + 0.5 * 1.05 * 140085.55 - 24400.0
  # 2018 bonus + 1/2 year at current salary + 1/2 year at 5% raise salary - standard deduction
convIncome = np.arange(0.0, 270000.0, 64.0)  # max is total IRA balance
stateTaxRate = 0.0425

# calculate the base tax and additional tax at each conversion value
baseTax = calculateFederalTaxes(baseIncome) + stateTaxRate * baseIncome
convTax = np.empty_like(convIncome)
for i in xrange(convIncome.size):
    convTax[i] = calculateFederalTaxes(baseIncome + convIncome[i]) + \
                 stateTaxRate * (baseIncome + convIncome[i]) - baseTax

# plot
matplotlib.rcParams.update({'font.size': 20, 'figure.facecolor': 'w', 'lines.linewidth': 2})

plt.figure()
plt.plot(convIncome / 1000.0, convTax / 1000.0)
plt.xlabel('converted balance ($k)')
plt.ylabel('additional income tax ($k)')
plt.grid()

plt.figure()
plt.plot(convIncome / 1000.0, convTax / convIncome)
plt.xlabel('converted balance ($k)')
plt.ylabel('cost per dollar converted')
plt.grid()