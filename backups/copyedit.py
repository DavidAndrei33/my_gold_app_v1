from flask import Blueprint, render_template, request, jsonify
from services.analysis_service import analyze_and_get_data, get_available_data_complete
from .forms import AnalysisForm
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

analysis_routes = Blueprint('analysis_routes', __name__)

# Restul codului existent

@analysis_routes.route('/get_analysis', methods=['POST'])
def get_analysis():
    # Extragerea datelor din cererea POST
    data = request.get_json()
    instrument = data['instrument']
    granularity = data['granularity']
    start_date = data['start_date']
    end_date = data['end_date']

    # Procesarea datelor și realizarea analizei tehnice
    result = analyze_and_get_data(instrument, granularity, start_date, end_date, data['indicators'])

    # Generarea graficului cu lumânări (candlestick patterns)
    candlestick_fig = create_candlestick_chart(result)  # Funcția create_candlestick_chart va fi definită mai jos

    # Salvarea rezultatelor într-un fișier CSV sau Excel
    save_results_to_file(result)  # Funcția save_results_to_file va fi definită mai jos

    return render_template('analysis_view.html', result=result, candlestick_fig=candlestick_fig)


def create_candlestick_chart(result):
    # Datele necesare pentru construirea graficului
    date = result['date']
    open_prices = result['open']
    high_prices = result['high']
    low_prices = result['low']
    close_prices = result['close']

    # Crearea unei figuri Plotly pentru graficul cu lumânări
    candlestick_fig = go.Figure(data=[go.Candlestick(x=date,
                                                     open=open_prices,
                                                     high=high_prices,
                                                     low=low_prices,
                                                     close=close_prices)])

    # Evidențierea modelelor de lumânări detectate pe grafic
    for pattern in result['candlestick_patterns']:
        # Dacă un anumit pattern este detectat, setăm culorile pentru acele date
        colors = ['green' if p == 1 else 'red' for p in pattern]
        
        # Adăugăm o serie de date pentru evidențierea pattern-ului pe grafic
        candlestick_fig.add_trace(go.Candlestick(x=date,
                                                 open=open_prices,
                                                 high=high_prices,
                                                 low=low_prices,
                                                 close=close_prices,
                                                 increasing_line_color=colors,
                                                 decreasing_line_color=colors))

    # Setăm titlurile și etichetele pentru axe
    candlestick_fig.update_layout(title='Candlestick Chart with Detected Patterns',
                                  xaxis_title='Date',
                                  yaxis_title='Price')

    return candlestick_fig

def save_results_to_file(result):
    # Creați aici codul pentru salvarea rezultatelor într-un fișier CSV sau Excel
    # Utilizați biblioteca pandas pentru a crea un DataFrame și a-l salva în fișier
    
    df = pd.DataFrame(result)  # Exemplu: rezultatele sunt stocate într-un dicționar
    df.to_csv('analysis_results.csv', index=False)  # Salvare în fișier CSV

    # Alternativ, puteți utiliza df.to_excel pentru salvare în Excel

# Restul codului existent


@analysis_routes.route('/get_analysis', methods=['POST'])
def get_analysis():
    # Extragerea datelor din cererea POST
    data = request.get_json()
    instrument = data['instrument']
    granularity = data['granularity']
    start_date = data['start_date']
    end_date = data['end_date']
    
    # Procesarea datelor și realizarea analizei tehnice
    result = analyze_and_get_data(instrument, granularity, start_date, end_date, data['indicators'])
    
    # Generarea graficului cu modelele de lumânări
    fig = go.Figure(data=[go.Candlestick(
        x=result['date'],
        open=result['open'],
        high=result['high'],
        low=result['low'],
        close=result['close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])

    # Adăugați aici cod pentru evidențierea modelelor de lumânări detectate
    
    # Actualizați aspectul graficului
    fig.update_layout(
        title='Candlestick Chart with Candlestick Patterns',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    # Salvați graficul într-un fișier HTML sau afișați-l în cadrul aplicației
    fig.write_html('candlestick_chart.html')

    # Salvarea rezultatelor într-un fișier CSV sau Excel
    df = pd.DataFrame(result)
    df.to_csv('analysis_results.csv', index=False)

    return render_template('analysis_view.html', result=result)


'https://www.cashbackforex.com/live-chart/datafeed/bars?symbol=CBOE-RUT&resolution=30&from=1691709560&to=1692893960&countback=329'

'https://www.cashbackforex.com/live-chart/datafeed/bars?symbol=CBOE:RUT?symbol=CBOE-RUT&resolution=30&from=1692575722&to=1693167922&countback=329'

https://www.cashbackforex.com/live-chart/datafeed/bars?symbol=CBOE:RUT&resolution=30&from=1692575722&to=1693167922&countback=329