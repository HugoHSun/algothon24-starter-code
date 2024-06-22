# import matplotlib
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
# import matplotlib.dates as mdates
# import numpy as np

# def graph():
#     data = np.loadtxt('prices.txt', dtype = float)
#     fig = plt.figure(figsize = (10,7))
#     ax1 = plt.subplot2grid((40,40), (0,0), rowspan = 40, colspan = 40)
    
#     ax1.plot()
# graph()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def loadPrices(fn):
    df = pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    return df.values

def plotPrices(prices, output_file):
    nInst, nt = prices.shape
    plt.figure(figsize=(12, 6))
    for i in range(nInst):
        plt.plot(prices[i], label=f'Instrument {i+1}')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.title('Price History of Instruments')
    # plt.legend(loc='upper left')
    plt.savefig(output_file)  # Save the plot as an image file
    plt.close()  # Close the plot to free up memory

# File containing the prices
pricesFile = "prices.txt"

# Load and transpose the data so that rows are instruments and columns are days
prcAll = loadPrices(pricesFile).T

# Specify the output file
output_file = "price_history.png"

# Plot the data and save it as an image
plotPrices(prcAll, output_file)