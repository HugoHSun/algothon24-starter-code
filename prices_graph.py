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
    plt.savefig(output_file)  # Save the plot as an image file
    plt.close()  # Close the plot to free up memory
pricesFile = "prices.txt"

prcAll = loadPrices(pricesFile).T
output_file = "price_history.png"

# Plot the data and save it as an image
plotPrices(prcAll, output_file)