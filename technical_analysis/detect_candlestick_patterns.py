import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd

def visualize_candlestick_patterns(df, patterns_df):
    fig, axes = mpf.plot(df, type='candle', style='charles', returnfig=True,
                         title='Candlestick Patterns',
                         ylabel='Price',
                         figsize=(15, 10))

    ax1 = axes[0]

    # Listă cu toate paternurile pe care dorim să le verificăm
    all_patterns = [
        'CDLENGULFING', 'CDLHAMMER', 'CDLDOJI', 'CDLHARAMI', 'CDLSHOOTINGSTAR', 
        # ... adaugă toate paternurile pe care dorești să le verifici
    ]

    for pattern in all_patterns:
        for index, row in patterns_df.iterrows():
            if row[pattern] != 0:
                color = 'g' if row[pattern] == 100 else 'r'
                ax1.annotate(pattern, xy=(mdates.date2num(index), df.loc[index]['Close']),
                             xytext=(mdates.date2num(index), df.loc[index]['High'] + 50),
                             arrowprops=dict(facecolor=color, arrowstyle='->'),
                             fontsize=8)

    mpf.show()


#df = pd.read_csv('path_to_your_data.csv', parse_dates=['Date'], index_col='Date')
#patterns_df = detect_candlestick_patterns(df)
#visualize_candlestick_patterns(df, patterns_df)


def detect_patterns(data: pd.DataFrame):
    # This function will detect the specified patterns and return their presence as a series of flags (True/False)

    # Ensure data is sorted by date (ascending)
    data = data.sort_values(by='Date')

    # Create empty flags for each pattern
    data['Doji'] = False
    data['Bullish_Engulfing'] = False
    data['Bearish_Engulfing'] = False
    data['Hammer'] = False
    data['Shooting_Star'] = False
    data['Morning_Star'] = False
    data['Evening_Star'] = False

    for i in range(1, len(data)-1):
        open_price, high, low, close_price = data.iloc[i][['Open', 'High', 'Low', 'Close']]

        # Detect Doji
        if abs(open_price - close_price) <= (high - low) * 0.1:  # Close and open are very close
            data.at[i, 'Doji'] = True

        # Detect Bullish Engulfing
        prev_open, prev_close = data.iloc[i-1][['Open', 'Close']]
        if prev_open > prev_close and open_price < close_price and open_price < prev_close and close_price > prev_open:
            data.at[i, 'Bullish_Engulfing'] = True

        # Detect Bearish Engulfing
        if prev_open < prev_close and open_price > close_price and open_price > prev_close and close_price < prev_open:
            data.at[i, 'Bearish_Engulfing'] = True

        # Detect Hammer
        if (high - max(open_price, close_price)) <= 2 * (min(open_price, close_price) - low) and (close_price - open_price) / (high - low) > 0.6:
            data.at[i, 'Hammer'] = True

        # Detect Shooting Star
        if (low - min(open_price, close_price)) <= 2 * (max(open_price, close_price) - high) and (open_price - close_price) / (high - low) > 0.6:
            data.at[i, 'Shooting_Star'] = True

        # Detect Morning Star
        prev2_open, prev2_close = data.iloc[i-2][['Open', 'Close']]
        if prev2_open > prev2_close and abs(prev_open - prev_close) <= (data.iloc[i-1]['High'] - data.iloc[i-1]['Low']) * 0.1 and open_price < close_price:
            data.at[i, 'Morning_Star'] = True

        # Detect Evening Star
        if prev2_open < prev2_close and abs(prev_open - prev_close) <= (data.iloc[i-1]['High'] - data.iloc[i-1]['Low']) * 0.1 and open_price > close_price:
            data.at[i, 'Evening_Star'] = True

    return data
