from flask import Blueprint, jsonify, current_app
from flask_pymongo import PyMongo
import os

financial_routes = Blueprint('financial', __name__)

DATA_PATH = os.path.join(current_app.root_path, 'data')


@financial_routes.route('/available_pairs', methods=['GET'])
def available_pairs():
    pairs = []
    for root, dirs, files in os.walk(DATA_PATH):
        for dir_name in dirs:
            if dir_name not in ['__pycache__']:
                pairs.append(dir_name)
    # Acest exemplu va returna toate directoarele din directorul "data" ca perechi disponibile.
    # Va trebui să ajustați această logică în funcție de structura exactă a directorului "data".
    return jsonify(pairs)


@financial_routes.route('/available_timeframes/<pair>', methods=['GET'])
def available_timeframes(pair):
    timeframes = []
    pair_path = os.path.join(DATA_PATH, pair)
    for root, dirs, files in os.walk(pair_path):
        for file_name in files:
            if file_name.endswith('.csv'):
                timeframes.append(file_name.replace('.csv', ''))
    # Acest exemplu va returna toate fișierele .csv din directorul specificat al perechii ca fiind timeframe-uri disponibile.
    return jsonify(timeframes)
