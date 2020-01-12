import numpy as np
import matplotlib.pyplot as plt


def getAutoRange(maxVal, label):
    if maxVal > 1.0e6:
        norm = 1.0e6
        label = label.replace('$', '$M')
    elif maxVal > 1.0e3:
        norm = 1.0e3
        label = label.replace('$', '$k')
    else:
        norm = 1.0

    return (norm, label)


def singlePlot(x, y, xLabel, yLabel):
    # initialize the plot
    plt.figure()

    # determine automatic range scaling
    (norm, yLabel) = getAutoRange(np.amax(np.fabs(y)), yLabel)

    # plot the series
    plt.plot(x, y / norm)

    # add labeling
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid(True)


def multiPlot(x, ys, xLabel, yLabel, yNames):
    # initialize the plot
    plt.figure()

    # determine automatic range scaling
    (norm, yLabel) = getAutoRange(np.amax(np.fabs(ys)), yLabel)

    # plot each y series
    for y in ys:
        plt.plot(x, y / norm)

    # add labeling
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend(yNames, loc="best")
    plt.grid(True)