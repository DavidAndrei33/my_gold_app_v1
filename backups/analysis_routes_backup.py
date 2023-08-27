from flask import Blueprint, render_template, request
from services.analysis_service import analyze_and_get_data
from .forms import AnalysisForm
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from services.analysis_service import analyze_and_get_data, get_available_currency_pairs

analysis_routes = Blueprint('analysis_routes', __name__)

@analysis_routes.route('/analyze', methods=['GET', 'POST'])
def analyze():
    form = AnalysisForm()
    if form.validate_on_submit():
        instrument = form.instrument.data
        granularity = form.granularity.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Process the selected indicators
        selected_indicators = {
            'moving_averages': form.moving_averages.data,
            'rsi': form.rsi.data,
            'macd': form.macd.data,
            'candlesticks': form.candlesticks.data
        }

        # Pass the selected indicators to the analysis function
        result = analyze_and_get_data(instrument, granularity, start_date, end_date, selected_indicators)
        
        return render_template('analysis_view.html', result=result)

    return render_template('analysis.html', form=form)

@analysis_routes.route('/analysis')
def analysis_view():
    # Încărcarea datelor
    data = pd.read_csv('data/eur_usd_data.csv')  # Ajustează calea dacă este necesar
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])

    # Inițializarea aplicației Dash
    dash_app = dash.Dash(__name__, server=analysis_routes, url_base_pathname='/dash/')
    dash_app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return render_template('analysis_view.html', form=AnalysisForm())

@analysis_routes.route('/analyze', methods=['GET', 'POST'])
def analyze():
    form = AnalysisForm()
    available_pairs = get_available_currency_pairs()  # Adaugă această linie

    if form.validate_on_submit():
        instrument = form.instrument.data
        granularity = form.granularity.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Process the selected indicators
        selected_indicators = {
            'moving_averages': form.moving_averages.data,
            'rsi': form.rsi.data,
            'macd': form.macd.data,
            'candlesticks': form.candlesticks.data
        }

        # Pass the selected indicators to the analysis function
        result = analyze_and_get_data(instrument, granularity, start_date, end_date, selected_indicators)
        
        return render_template('analysis_view.html', result=result)

    return render_template('analysis.html', form=form, available_pairs=available_pairs)  # Modifică această linie
