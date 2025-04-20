import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Preview data for each ticker
def preview_stock_data(ticker: str, df: pd.DataFrame):
    print(f"Head of {ticker} dataframe: ")
    print(df.head())
    print(f"Summary stats for {ticker}")
    print(df.describe())
    print('\n')
    
# Plot stock closing price
def plot_stock_price(ticker: str, df: pd.DataFrame) -> plt.figure:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Close'])
    ax.set_title(f'{ticker} Stock Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')
    ax.grid(True)
    return fig

# Plot the 30 and 90 days moving averages for a stock price
def plot_rolling_stats(ticker: str, df: pd.DataFrame) -> plt.figure:
    df['MA30'] = df['Close'].rolling(window=30).mean()
    df['MA90'] = df['Close'].rolling(window=90).mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df[['Close', 'MA30', 'MA90']])
    ax.set_title(f'{ticker}: Price vs Moving Average')
    ax.grid(True)
    return fig

# Plot the stocks returns
def plot_stock_returns(ticker: str, df: pd.DataFrame) -> plt.Figure:
    df = df.copy()  # To avoid modifying the original DataFrame
    df['Returns'] = df['Close'].pct_change()

    fig, ax = plt.subplots(figsize=(10, 5))
    df['Returns'].hist(bins=100, ax=ax)
    ax.set_title(f'Daily Returns Distribution for {ticker}')
    ax.set_xlabel('Daily Return')
    ax.set_ylabel('Frequency')

    return fig

def plot_seasonal_decomposition(ticker: str, df: pd.DataFrame) -> plt.Figure:
    plt.figure(figsize=(12, 6))
    result = seasonal_decompose(df['Close'], model='multiplicative', period=252)
    
    fig = result.plot()
    fig.suptitle(f"{ticker} - Seasonal Decomposition of Closing Prices", fontsize=14)
    
    plt.tight_layout()
    return fig
    
if __name__ == '__main__':
    tickers = ['AAPL', 'AMZN', 'GOOGL', 'META', 'NFLX']
    dfs = {}
    os.makedirs('images', exist_ok=True)

    for ticker in tickers:
        df = pd.read_csv(f'data/{ticker}.csv')
        preview_stock_data(ticker, df)
        # plot stock price
        fig = plot_stock_price(ticker, df)
        fig.savefig(f'images/{ticker}_stock_price.png')
        plt.close(fig)
        # plot moving averages
        fig = plot_rolling_stats(ticker, df)
        fig.savefig(f'images/{ticker}_rolling_stats.png')
        plt.close(fig)
        # plot stock daily returns
        fig = plot_stock_returns(ticker, df)
        fig.savefig(f'images/{ticker}_returns_distribution.png')
        plt.close(fig)
        # plot seasonal decomposition
        fig = plot_seasonal_decomposition(ticker, df)
        fig.savefig(f'images/{ticker}_seasonal_decomposition.png')
        plt.close(fig)