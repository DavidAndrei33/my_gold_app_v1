from flask import Blueprint, render_template, jsonify, current_app
from flask_pymongo import PyMongo
import os

financial_routes = Blueprint('financial', __name__, template_folder='templates')

# Ruta deja existentă pentru available_pairs
@financial_routes.route('/available_pairs', methods=['GET'])
def available_pairs():
    # Listăm directoarele din directorul 'data' pentru a obține pair-urile.
    pairs = [d for d in os.listdir(current_app.root_path + '/data') if os.path.isdir(os.path.join(current_app.root_path + '/data', d))]
    return jsonify(pairs)

@financial_routes.route('/available_timeframes/<pair>', methods=['GET'])
def get_available_timeframes(pair):
    # Listăm toate fișierele CSV din directorul specific pair-ului pentru a obține timeframe-urile.
    timeframes = [f.split('.')[0] for f in os.listdir(os.path.join(current_app.root_path + '/data', pair)) if f.endswith('.csv')]
    return jsonify(timeframes)
