from pymongo import MongoClient, ASCENDING

# Conectare la MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.my_gold_app_db
historical_data_collection = db.historical_data

# Crearea unui index unic compus pentru data, ora și numele perechii
historical_data_collection.create_index(
    [("time", ASCENDING), ("symbol", ASCENDING)],
    unique=True
)
