import pandas_ta as ta
import pandas as pd

def detect_candlestick_patterns(df):
    # Calculating candlestick patterns using pandas-ta
    df.ta.cdl_pattern()

    patterns = [
        "DOJI",
        "HAMMER",
        "INVERTEDHAMMER",
        "SHOOTINGSTAR",
        "HANGINGMAN",
        "BULLISHENGULFING",
        "BEARISHENGULFING",
        "MORNINGSTAR",
        "EVENINGSTAR",
        "3BLACKCROWS",
        "3WHITESOLDIERS",
        "PIERCING",
        "DARKCLOUDCOVER"
    ]
    
    detected_patterns = {}
    for pattern in patterns:
        if df[pattern].iloc[-1] == 1:
            detected_patterns[pattern] = "Bullish Signal"
        elif df[pattern].iloc[-1] == -1:
            detected_patterns[pattern] = "Bearish Signal"
    
    return detected_patterns

# Test the function with your dataframe
# For example:
# detected_patterns = detect_candlestick_patterns(df)
# print(detected_patterns)
