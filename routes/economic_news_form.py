from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class EconomicNewsForm(FlaskForm):
    news_content = TextAreaField('Introduceți știrile economice:', validators=[DataRequired()])
    submit = SubmitField('Analizează')
