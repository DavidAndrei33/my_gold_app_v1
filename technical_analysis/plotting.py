
import pandas as pd
import mplfinance as mpf

def plot_candlestick_chart(data_path, save_path=None):
    """
    Plot and save a candlestick chart using mplfinance.
    
    Parameters:
    - data_path (str): Path to the CSV file containing the data.
    - save_path (str, optional): Path to save the plot. If not provided, the plot will be displayed.
    
    Returns:
    - None
    """
    
    # Load the data
    df = pd.read_csv(data_path, parse_dates=['time'], index_col='time')
    
    # Create the plot
    mpf.plot(df, type='candle', style='charles', title='XAU/USD 5m',
             ylabel='Price', volume=True, mav=(5,10), savefig=save_path)
