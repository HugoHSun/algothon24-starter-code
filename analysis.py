import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# **********Correlation Analysis**********
# Plot the correlation matrix as a heatmap
def plot_corr_matrix(corr_matrix):
    fig, ax = plt.subplots(figsize=(20, 18), layout='constrained')
    ax.set_title('Stocks Correlation Matrix')
    sns.heatmap(corr_matrix, ax=ax, annot=True, fmt='.2f', annot_kws={'size': 7}, center=0, cmap='coolwarm')
    plt.savefig(output_dirs[1] + 'correlation_matrix.pdf')


# Detect highly correlated stocks
def analyse_high_corr_stocks(corr_matrix, corr_threshold):
    high_corr_stocks = {}
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            if i == j:
                continue
            elif abs(corr_matrix[i][j]) >= corr_threshold:
                if i not in high_corr_stocks.keys():
                    high_corr_stocks[i] = set()
                high_corr_stocks[i].add((j, corr_matrix[i][j]))

    with open(output_dirs[1] + 'high_correlation_stocks.txt', 'w') as f:
        for key, value in high_corr_stocks.items():
            value = sorted(value, key=lambda stock: stock[0])
            f.write(f"stock {key}: {value}\n")

            fig, ax = plt.subplots(layout='constrained')
            ax.set_title(f"Stock {key} Prices with Highly Correlated Stocks")
            ax.set_xlabel('time')
            ax.set_ylabel('price')
            ax.plot(prices[key], label=f"stock {key}")
            for i in range(len(value)):
                ax.plot(prices[value[i][0]], label=f"stock {value[i][0]}, corr {value[i][1]}")
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.savefig(output_dirs[2] + f"stock_{key}.jpg", dpi=800)


# **********Correlation Analysis**********

if __name__ == "__main__":
    prices = pd.read_csv('prices.txt', delimiter='\s+', header=None)
    corr_matrix = round(prices.corr(), 2)
    corr_threshold = 0.9

    output_dirs = ['./data_analysis/', './data_analysis/correlations/',
                   './data_analysis/correlations/correlated_price_graphs/']
    for dire in output_dirs:
        if not os.path.isdir(dire):
            os.makedirs(dire)

    plot_corr_matrix(corr_matrix)
    analyse_high_corr_stocks(corr_matrix, corr_threshold)
