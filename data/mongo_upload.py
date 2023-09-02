import os
import pandas as pd
from pymongo import MongoClient

# Conectare la MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.my_gold_app_db
historical_data_collection = db.historical_data

# Calea către folderul care conține toate perechile (înlocuiește cu calea ta)
root_folder_path = "D:\\GitHub\\my_gold_app\\data"

# Parcurgerea fiecărui folder de pereche
for pair_folder in os.listdir(root_folder_path):
    pair_folder_path = os.path.join(root_folder_path, pair_folder)
    
    # Verificarea dacă este un folder
    if os.path.isdir(pair_folder_path):
        
        # Parcurgerea fiecărui fișier CSV din folderul perechii
        for csv_file in os.listdir(pair_folder_path):
            if csv_file.endswith('.csv'):
                csv_file_path = os.path.join(pair_folder_path, csv_file)
                
                # Citirea datelor din CSV
                df = pd.read_csv(csv_file_path)
                
                # Extragerea time-frame-ului din numele fișierului (presupunând că numele fișierului este time-frame-ul)
                timeframe = csv_file.split('.')[0]
                
                # Verificarea existenței coloanei 'symbol' înainte de a o elimina
                if 'symbol' in df.columns:
                    df = df.drop(columns=['symbol'])
                
                # Actualizarea datelor în MongoDB
                historical_data_collection.update_one(
                    {"symbol": pair_folder, "timeframe": timeframe},
                    {"$push": {"data": {"$each": df.to_dict('records')}}},
                    upsert=True
                )

print("Datele au fost încărcate în MongoDB.")
