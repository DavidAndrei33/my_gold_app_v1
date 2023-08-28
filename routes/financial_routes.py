from flask import Blueprint, jsonify
from flask_pymongo import PyMongo
from analysis import apply_strategy
import os
from flask import current_app 
financial_routes = Blueprint('financial', __name__)


@financial_routes.route('/available_pairs', methods=['GET'])
def available_pairs():
    DATA_PATH = os.path.join(current_app.root_path, 'data')
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
    DATA_PATH = os.path.join(current_app.root_path, 'data')
    timeframes = []
    pair_path = os.path.join(DATA_PATH, pair)
    for root, dirs, files in os.walk(pair_path):
        for file_name in files:
            if file_name.endswith('.csv'):
                timeframes.append(file_name.replace('.csv', ''))
    # Acest exemplu va returna toate fișierele .csv din directorul specificat al perechii ca fiind timeframe-uri disponibile.
    return jsonify(timeframes)

@financial_routes.route('/analyze')
def analyze():
    pair = request.args.get('pair')
    timeframe = request.args.get('timeframe')
    
    result = apply_strategy(pair, timeframe)
    
    # Aici poți procesa rezultatele și returna un răspuns către interfața grafică
    return jsonify(result.tail(10).to_dict(orient="records"))
