import requests
import pandas as pd
import os

# Solicită timeframe-ul
timeframe = input("Introduceți timeframe-ul (de ex. 5m, 15m, 30m, 60m): ")

# Construiește URL-ul complet pentru CBOE:RUT folosind linkul oferit de dvs.
url = f"https://www.cashbackforex.com/live-chart/datafeed/bars?symbol=CBOE:RUT&resolution={timeframe}&from=1692575722&to=1693167922&countback=329"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

# Verificăm dacă cererea a avut succes
if response.status_code == 200:
    data = response.json()
    
    # Creăm un DataFrame din date
    df = pd.DataFrame(data)
    
    # Convertim timestamp-ul într-o dată și oră în format standard
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    print(data)
    print(df.head())
    print(df.columns)

    # Înlocuim ':' cu '_' pentru a evita eroarea
    directory_name = 'CBOE_RUT'
    directory = f'my_gold_app/my_gold_app/my_gold_app/data/{directory_name}'

    # Verificăm dacă rădăcina căii există, dacă nu, o creăm
    root_path = 'my_gold_app/my_gold_app/my_gold_app/data/'
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    # Asigurați-vă că folderul pentru pereche există
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Salvăm DataFrame-ul ca fișier CSV în folderul specific pentru acea pereche
    path = f"{directory}/{timeframe}.csv"
    df.to_csv(path, index=False)
    print(f"Datele au fost salvate cu succes în {path}!")
    print(df.head())
else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
