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
    plt.close(fig)


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

            fig_price, ax_price = plt.subplots(num=1, layout='constrained')
            fig_pct, ax_pct = plt.subplots(num=2, figsize=(16, 10), layout='constrained')
            ax_price.set_title(f"Stock {key} Prices with Highly Correlated Stocks")
            ax_pct.set_title(f"Stock {key} Prices with Highly Correlated Stocks")
            ax_price.set_xlabel('time')
            ax_pct.set_xlabel('time')
            ax_price.set_ylabel('price')
            ax_pct.set_ylabel('percentage change')
            ax_price.plot(prices[key], label=f"stock {key}")
            ax_pct.plot(prices_pct[key], label=f"stock {key}")
            for i in range(len(value)):
                ax_price.plot(prices[value[i][0]], label=f"stock {value[i][0]}, corr: {value[i][1]}")
                ax_pct.plot(prices_pct[value[i][0]], label=f"stock {value[i][0]}, corr: {value[i][1]}", linewidth=1)
            ax_price.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            ax_pct.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            if not os.path.isdir(output_dirs[2] + f"stock{key}/"):
                os.makedirs(output_dirs[2] + f"stock{key}/")
            plt.figure(1)
            plt.savefig(output_dirs[2] + f"stock{key}/stock_{key}.jpg", dpi=500)
            plt.figure(2)
            plt.savefig(output_dirs[2] + f"stock{key}/stock_{key}_pct.jpg", dpi=500)
            plt.close(fig_price)
            plt.close(fig_pct)


# **********Correlation Analysis**********

if __name__ == "__main__":
    prices = pd.read_csv('prices.txt', delimiter='\s+', header=None)
    prices_pct = prices.pct_change()
    corr_matrix = round(prices.corr(), 2)
    prices_stat = []
    corr_threshold = 0.9

    output_dirs = ['./data_analysis/', './data_analysis/correlations/',
                   './data_analysis/correlations/correlated_price_graphs/']
    for dire in output_dirs:
        if not os.path.isdir(dire):
            os.makedirs(dire)

    # Plot all the stock prices
    fig_price, ax_price = plt.subplots(num=1, figsize=(14, 12), layout='constrained')
    fig_pct, ax_pct = plt.subplots(num=2, figsize=(20, 12), layout='constrained')
    ax_price.set_title('Stock Prices')
    ax_pct.set_title('Stock Prices Percentage Change')
    ax_price.set_xlabel('time')
    ax_pct.set_xlabel('time')
    ax_price.set_ylabel('price')
    ax_pct.set_ylabel('percentage change')
    stat_output = open(output_dirs[0] + "stock_stats.txt", "w")
    for i in range(len(prices.columns)):
        stat_output.write(f"stock {i} - mean: {prices[i].mean():.2f} std: {prices[i].std():.2f}\n")
        ax_price.plot(prices[i], label=f"stock {i}")
        ax_pct.plot(prices_pct[i], label=f"stock {i}", linewidth=0.8)
    stat_output.close()
    ax_price.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax_pct.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.figure(1)
    plt.savefig(output_dirs[0] + "stock_prices.pdf")
    plt.figure(2)
    plt.savefig(output_dirs[0] + "stock_prices_pct.pdf")
    plt.close(fig_price)
    plt.close(fig_pct)

    plot_corr_matrix(corr_matrix)
    analyse_high_corr_stocks(corr_matrix, corr_threshold)
