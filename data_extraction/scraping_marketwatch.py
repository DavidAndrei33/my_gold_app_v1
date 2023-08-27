import requests
import pandas as pd
import os

# URL-ul de bază
BASE_URL = "https://www.cashbackforex.com/live-chart/datafeed/bars"

# Definirea perechilor și a identificatorilor lor
PAIRS = {
    "xau/usd": "IC MARKETS:10012"
    # Puteți adăuga mai multe perechi aici
}

# Definirea rezoluției pentru timeframes
TIMEFRAMES = {
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "60m": 60
}

# Solicită simbolul/perechea
pair = input("Introduceți perechea (de ex. xau/usd): ").lower()
if pair not in PAIRS:
    custom_symbol = input("Introduceți identificatorul personalizat pentru această pereche: ")
    PAIRS[pair] = custom_symbol

# Solicită timeframe-ul
timeframe = input("Introduceți timeframe-ul (de ex. 5m, 15m, 30m, 60m): ").lower()

# Construiește URL-ul complet
url = f"{BASE_URL}?symbol={PAIRS[pair]}&resolution={TIMEFRAMES[timeframe]}&from=1691709560&to=1692893960&countback=329"

response = requests.get(url)

# Verificăm dacă cererea a avut succes
if response.status_code == 200:
    data = response.json()
    
    # Creăm un DataFrame din date
    df = pd.DataFrame(data)
    
    # Convertim timestamp-ul într-o dată și oră în format standard
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    
    # Asigurați-vă că folderul pentru pereche există
    directory = f'my_gold_app/my_gold_app/my_gold_app/data/{pair}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Salvăm DataFrame-ul ca fișier CSV în folderul specific pentru acea pereche
    path = f"{directory}/{timeframe}.csv"
    df.to_csv(path, index=False)
    print(f"Datele au fost salvate cu succes în {path}!")
else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
xauu