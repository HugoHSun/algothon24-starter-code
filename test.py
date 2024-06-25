import pandas as pd
import matplotlib.pyplot as plt

prices = pd.read_csv('prices.txt', delimiter='\s+', header=None)
prices_pct = prices.pct_change()

prices.plot()
prices_pct.plot()
plt.show()
