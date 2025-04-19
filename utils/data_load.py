import yfinance as yf
import pandas as pd
import os

# FAANG tickers
tickers = {
    'META': 'Meta Platforms',
    'AAPL': 'Apple',
    'AMZN': 'Amazon',
    'NFLX': 'Netflix',
    'GOOGL': 'Alphabet'
}

def download_faang_data(start='2015-01-01', end='2024-12-31', save_dir='data'):
    os.makedirs(save_dir, exist_ok=True)
    faang_data = {}

    for ticker, name in tickers.items():
        print(f"Downloading {name} ({ticker}) data...")
        df = yf.download(ticker, start=start, end=end)[['Close']].dropna()
        df.columns = ['Close']
        faang_data[ticker] = df
        df.to_csv(os.path.join(save_dir, f"{ticker}.csv"))
    
    print("Download complete.")
    return faang_data

if __name__ == "__main__":
    download_faang_data()
