import pandas as pd
import plotly.graph_objects as go

# Încarcă datele din fișierul CSV
data = pd.read_csv('data/xau-usd/5m.csv')

# Convertim coloana 'time' la tipul dată
data['time'] = pd.to_datetime(data['time'])

# Creăm figura folosind subplots pentru graficul de prețuri și pentru indicatorul de volum
fig = go.Figure()

# Adăugăm graficul de prețuri
fig.add_trace(go.Candlestick(x=data['time'],
                             open=data['open'],
                             high=data['high'],
                             low=data['low'],
                             close=data['close'],
                             name='Lumânări japoneze'))

# Adăugăm indicatorul de volum
fig.add_trace(go.Bar(x=data['time'],
                     y=data['volume'],
                     name='Volum'))

# Configurăm aspectul și funcționalitățile graficului
fig.update_layout(title='Grafic de Prețuri și Volum',
                  xaxis_rangeslider_visible=True,  # Activăm slider-ul de zoom
                  xaxis=dict(rangeselector=dict(buttons=list([
                          dict(count=1, label='1d', step='day', stepmode='backward'),
                          dict(count=7, label='1w', step='day', stepmode='backward'),
                          dict(count=1, label='1m', step='month', stepmode='backward'),
                          dict(step='all')
                      ])),
                      rangeslider=dict(visible=True),
                      type='date'
                  )
              )

# Afișăm graficul
fig.show()
