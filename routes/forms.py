from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField, SelectField, validators
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from wtforms import TextAreaField, SubmitField
from wtforms import BooleanField, StringField, SubmitField
print("Inside forms.py")

class MarketDataForm(FlaskForm):
    currency_pair = SelectField('Selectați perechea valutară:', choices=['xau/usd', 'eur/usd', 'usd/jpy'])
    timeframe = SelectField('Selectați perioada de timp:', choices=['5m', '30m', '1h', '4h', '1d'])
    date = DateField('Data', [validators.InputRequired()])
    price = FloatField('Preț', [validators.InputRequired()])
    volume = IntegerField('Volum', [validators.InputRequired()])
    asset_type = SelectField('Tipul de Activ', choices=[('gold', 'Aur'), ('silver', 'Argint')], validators=[validators.InputRequired()])

class NewsForm(FlaskForm):
    news_content = TextAreaField('Introduceți știrile:', validators=[DataRequired()])
    submit = SubmitField('Analizează')

class AnalysisForm(FlaskForm):
    instrument = StringField('Instrument', validators=[DataRequired()])
    granularity = StringField('Granularity', validators=[DataRequired()])
    start_date = StringField('Start Date (YYYY-MM-DD)', validators=[DataRequired()])
    end_date = StringField('End Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Analyze')
    moving_averages = BooleanField('Moving Averages')
    rsi = BooleanField('RSI (Relative Strength Index)')
    macd = BooleanField('MACD (Moving Average Convergence Divergence)')
    candlesticks = BooleanField('Candlestick Patterns')
