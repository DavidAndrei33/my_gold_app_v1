import pandas as pd
import numpy as np
import os

def calculate_technical_indicators(data):
    # Calculul RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Calculul CCI
    TP = (data['High'] + data['Low'] + data['Close']) / 3
    data['CCI'] = (TP - TP.rolling(window=20).mean()) / (0.015 * TP.rolling(window=20).std())

    # Calculul ATR
    data['ATR'] = data['High'] - data['Low']

    # Semnale de cumpărare sau vânzare
    data['Signal'] = np.where((data['RSI'] < 30) | (data['CCI'] < -100), 'Buy', 
                              np.where((data['RSI'] > 70) | (data['CCI'] > 100), 'Sell', 'Neutral'))

    return data

def load_data(pair, timeframe):
    file_path = os.path.join("data", pair, f"{timeframe}.csv")
    data = pd.read_csv(file_path)
    return data


def apply_strategy(pair, timeframe):
    data = load_data(pair, timeframe)
    data_with_indicators = calculate_technical_indicators(data)
    return data_with_indicators

# Exemplu de utilizare
pair = "EURUSD"  # De exemplu
timeframe = "60"  # De exemplu
#result = apply_strategy(pair, timeframe)
#print(result[['Close', 'RSI', 'CCI', 'ATR', 'Signal']].tail(10))
