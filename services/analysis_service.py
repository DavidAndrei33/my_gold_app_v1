from models.market_data import HistoricalData
import pandas as pd
import os
import sys
sys.path.append('d:/GitHub/my_gold_app')

def get_available_data_complete():   
    data_path = "data"
    available_data = {
        "pairs": [],
        "timeframes": {}
    }

    # Iterate over the directories (currency pairs) inside the "data" directory
    for root, dirs, files in os.walk(data_path):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            
            # Convert directory structure to pair name using '-'
            pair = directory_path.replace(data_path + '/', '').replace('/', '-')
            
            # Extract timeframes from the file names
            timeframes = []
            for file in os.listdir(directory_path):
                if file.endswith(".csv"):
                    # Assuming the naming convention is like "5m.csv", "1h.csv" etc.
                    timeframe = file.split('.')[0]
                    timeframes.append(timeframe)

            if pair not in available_data["pairs"]:
                available_data["pairs"].append(pair)
            
            if pair not in available_data["timeframes"]:
                available_data["timeframes"][pair] = []
            available_data["timeframes"][pair].extend(timeframes)

    return available_data
    data_path = "data"
    available_data = {
        "pairs": [],
        "timeframes": {}
    }

    # Iterate over the directories (currency pairs) inside the "data" directory
    for directory in os.listdir(data_path):
        directory_path = os.path.join(data_path, directory)
        
        # Check if it's a directory
        if os.path.isdir(directory_path):
            available_data["pairs"].append(directory)

            # Extract timeframes from the file names
            timeframes = []
            for file in os.listdir(directory_path):
                if file.endswith(".csv"):
                    # Assuming the naming convention is like "5m.csv", "1h.csv" etc.
                    timeframe = file.split('.')[0]
                    timeframes.append(timeframe)

            available_data["timeframes"][directory] = timeframes

    return available_data

def get_available_data():
    data_path = "data"
    available_data = {
        "pairs": [],
        "timeframes": {}
    }

    # Iterate over the directories (currency pairs) inside the "data" directory
    for directory in os.listdir(data_path):
        directory_path = os.path.join(data_path, directory)
        
        # Check if it's a directory
        if os.path.isdir(directory_path):
            available_data["pairs"].append(directory)

            # Extract timeframes from the file names
            timeframes = []
            for file in os.listdir(directory_path):
                if file.endswith(".csv"):
                    # Assuming the naming convention is like "5m.csv", "1h.csv" etc.
                    timeframe = file.split('.')[0]
                    timeframes.append(timeframe)

            available_data["timeframes"][directory] = timeframes

    return available_data

def calculate_moving_averages(data, periods=[50, 200]):
    for period in periods:
        column_name = f"SMA_{period}"
        data[column_name] = data['Close'].rolling(window=period).mean()
    return data

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    data['RSI'] = rsi
    return data

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    data['MACD'] = short_ema - long_ema
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

def analyze_and_get_data(instrument, granularity, start_date, end_date, selected_indicators):
    # Obține datele de piață pentru instrumentul selectat și perioada specificată
    # Presupunând că ai o metodă pentru a obține aceste date, de exemplu:
    data = HistoricalData.get_data(instrument, granularity, start_date, end_date)

    results = {}
    
    if selected_indicators['moving_averages']:
        results['moving_averages'] = calculate_moving_averages(data)
    
    if selected_indicators['rsi']:
        results['rsi'] = calculate_rsi(data)
    
    if selected_indicators['macd']:
        results['macd'] = calculate_macd(data)
    
    if selected_indicators['candlesticks']:
        # Pentru moment, las această parte necompletată
        # results['candlesticks'] = detect_candlestick_patterns(data)
        pass
    
    return results
