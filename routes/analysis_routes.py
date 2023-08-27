from flask import Blueprint, render_template, request
from services.analysis_service import analyze_and_get_data
from .forms import AnalysisForm
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from services.analysis_service import analyze_and_get_data, get_available_data_complete

analysis_routes = Blueprint('analysis_routes', __name__)

@analysis_routes.route('/analyze', methods=['GET', 'POST'])

@analysis_routes.route('/available_files', methods=['GET'])
def available_files():
    data_path = "data"
    available_files = []

    # Obține lista numelor fișierelor din directorul "data"
    for file in os.listdir(data_path):
        if os.path.isfile(os.path.join(data_path, file)):
            available_files.append(file)

    return render_template('available_files.html', available_files=available_files)

def analyze():
    form = AnalysisForm()
    available_pairs = get_available_data_complete()  # Obține perechile valutare disponibile

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

    return render_template('analysis.html', form=form, available_pairs=available_pairs)
print("Analysis service module loaded!")

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

@analysis_routes.route('/get_analysis', methods=['POST'])
def get_analysis():
    # Extragerea datelor din cererea POST
    data = request.get_json()
    instrument = data['instrument']
    timeframe = data['timeframe']    
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

