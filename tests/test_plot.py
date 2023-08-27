from services.analysis_service import analyze_and_plot_data
import pandas as pd

# Încărcăm datele CSV
df = pd.read_csv('data/xau/usd/5m.csv')

# Convertim coloana 'time' la format datetime
df['time'] = pd.to_datetime(df['time'])

# Redenumim coloanele pentru a se potrivi cu cerințele mplfinance
df = df.rename(columns={'time': 'Date', 'close': 'Close', 'open': 'Open', 'high': 'High', 'low': 'Low', 'volume': 'Volume'})
df = df.set_index('Date')

# Apelăm funcția de analiză și vizualizare
analyze_and_plot_data(df)
analyze_and_plot_data("data/xau/usd/5m.csv")
