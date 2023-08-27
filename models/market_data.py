from datetime import datetime
from pymongo import MongoClient

# Configurare conexiune cu baza de date MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.my_gold_app_db
instruments_collection = db.instruments
historical_data_collection = db.historical_data

class Instrument:
    @staticmethod
    def add_instrument(name, description):
        """
        Adaugă un nou instrument.
        """
        return instruments_collection.insert_one({
            "name": name,
            "description": description,
            "created_at": datetime.utcnow()
        }).inserted_id

    @staticmethod
    def get_by_name(name):
        """
        Returnează instrumentul după nume.
        """
        return instruments_collection.find_one({"name": name})

class HistoricalData:
    @staticmethod
    def add_data(instrument_id, date, price, volume):
        """
        Adaugă date istorice pentru un instrument.
        """
        historical_data_collection.insert_one({
            "instrument_id": instrument_id,
            "date": date,
            "price": price,
            "volume": volume,
            "created_at": datetime.utcnow()
        })

    @staticmethod
    def get_data_by_instrument(instrument_id):
        """
        Returnează toate datele istorice pentru un instrument specific.
        """
        return list(historical_data_collection.find({"instrument_id": instrument_id}))
