'''
==== MARIO - priMAry useR arrIvals data generatOr ====

This script is intended to generate simulation data regarding the Primary Users
behavior in the cognitive radio context.
The arrivals are distributed as a Poisson Process, whereas transmission duration
of each PU fits a normal distribution.
'''

import pandas as pd
import random as rd
import numpy as np
import matplotlib as matplotlib
import matplotlib.pyplot as plt


# Interface banner
def initialBanner():
    print("==============================================")
    print(" MARIO - priMAry useR arrIvals data generatOr ")
    print("==============================================")


# User input to define the duration of simulation
def simuDuration():
    print("--> Max simulation duration: 24h (1440 min)")
    maxSimuDuration = 60 * int(input("Set the simulation duration [h]: "))

    if maxSimuDuration > 1440:
        print("The max simulation duration should be up to 24h." +
              "\nPlease, try again.")
        simuDuration()

    return maxSimuDuration


# User input to define the number of channels to simulate
def numberOfChannels():
    numOfChannels = int(input("Set the number of channels: "))
    return numOfChannels


# The lambda value defines the average time between the PUs arrivals.
def lambdaValue():
    lambdaSize = 1 / int(input("A PU arrival must occur" +
                               " once every X minutes: "))
    return lambdaSize


# User input of the average duration of transmission for each arrival
def avgTransDuration():
    transDuration = int(input("Set average transmission duration [min]: "))
    return transDuration


# Poisson process generation
def poissonProcess(maxSimuDuration, transDuration, lambdaSize):
    randDuration = 0
    puArrivals = [0] * maxSimuDuration  # This list stores the simulation data
    u = 0

    while randDuration < maxSimuDuration:
        # To achieve Poisson Process, the arrivals are ditributed exponentially
        randArrival = rd.expovariate(lambdaSize) + randDuration
        # Whereas the duration of transmission fits a normal distribution
        randDuration = randArrival + rd.randint(2, transDuration)

        # The transmission period is set as 1
        for x in range(int(randArrival), int(randDuration)):
            if x < maxSimuDuration:
                puArrivals[x] = 1

        u += 1

    return puArrivals


# Converts the simulation data to the plot format
def dataConversion(puArrivals):
    auxTupleList = []

    x = 0
    while x < len(puArrivals):
        if puArrivals[x] == 1:
            iniTuple = x
            endTuple = 0

            while (x < len(puArrivals)) and (puArrivals[x] == 1):
                x += 1
                endTuple += 1
            auxTuple = (iniTuple, endTuple)
            auxTupleList.append(auxTuple)

        x += 1

    return auxTupleList


# Frequency of each tick in the plot x-axis
def tickFreq(maxSimuDuration):
    aux = None
    if 1 <= maxSimuDuration <= 60:
        aux = 20

    elif 61 <= maxSimuDuration <= 300:
        aux = 30
    elif 301 <= maxSimuDuration <= 800:
        aux = 60

    else:
        aux = 120

    return aux


# Plot function
def plotTimeLine(channelList, numOfChannels, maxSimuDuration):
    aux = input("Would you like to save the data plot? (Y/N): ")

    if (aux == 'Y') or (aux == 'y'):
        plot_font = {'fontname': 'Liberation Serif'}
        aux = input("Please, set the file name: ")
        fig, ax = plt.subplots()
        yTickList = []
        yLabelList = []
        pos = 0

        for x in range(0, numOfChannels):
            ax.broken_barh(channelList[x], (pos, 1),
                           facecolors='C%d' % (x % 10))
            yTickList.append(0.5 + pos)
            yLabelList.append(x + 1)
            pos += 2

        plt.xticks(np.arange(0, maxSimuDuration +
                             1, tickFreq(maxSimuDuration)), **plot_font)
        ax.set_xlim(0, maxSimuDuration)
        ax.set_xlabel('Timeline [min]', **plot_font)
        ax.set_ylabel('Channels', **plot_font)
        ax.set_yticks(yTickList)
        ax.set_yticklabels(yLabelList, **plot_font)
        ax.grid(True)
        plt.title("PUs arrivals timeline", **plot_font)
        plt.savefig((aux + '.pdf'), bbox_inches='tight', dpi=1250)

    elif (aux == 'N') or (aux == 'n'):
        print("Did not save the figure.")

    else:
        print("Unknown option.")
        plotTimeLine(channelList, numOfChannels, maxSimuDuration)


# Functino to generate the data frame and csv file containing simulation data
def csvGenerator(puArrivals, numOfChannels, maxSimuDuration):
    aux = input("Would you like to save the simulation data into csv? (Y/N): ")

    if (aux == 'Y') or (aux == 'y'):
        aux = input("Please, set the file name: ")
        csvData = dict()
        columnNames = [0] * numOfChannels

        for x in range(0, numOfChannels):
            columnNames[x] = 'Channel %d' % (x + 1)
            csvData.update({columnNames[x]: puArrivals[x]})

        df = pd.DataFrame(csvData, columns=columnNames)
        df.index.name = 'Minutes'
        df.to_csv((aux + '.csv'))

    elif (aux == 'N') or (aux == 'n'):
        print("Did not save the data.")

    else:
        print("Unknown option.")
        csvGenerator(puArrivals, numOfChannels, maxSimuDuration)


# Main function
def main():
    initialBanner()  # Calls the interface banner
    maxSimuDuration = simuDuration()  # Max duration of the simulation [min]
    numOfChannels = numberOfChannels()  # THe number of channels to simulate

    # Lists initialization
    puArrivals = [[0] * numOfChannels] * maxSimuDuration
    channelList = [[0] * numOfChannels] * maxSimuDuration
    lambdaSize = [0] * numOfChannels
    transDuration = [0] * numOfChannels

    # Parameters of each channel
    for x in range(0, numOfChannels):
        print("=======================================")
        print("       Channel %d parameters" % (x + 1))
        lambdaSize[x] = lambdaValue()
        transDuration[x] = avgTransDuration()
        puArrivals[x] = poissonProcess(maxSimuDuration, transDuration[x],
                                       lambdaSize[x])
        channelList[x] = dataConversion(puArrivals[x])

    # Generates csv
    csvGenerator(puArrivals, numOfChannels, maxSimuDuration)
    # Generates the plot image
    plotTimeLine(channelList, numOfChannels, maxSimuDuration)

if __name__ == "__main__":
    main()
