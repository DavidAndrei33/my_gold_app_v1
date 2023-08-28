
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.market_data import Instrument, HistoricalData
from .forms import MarketDataForm, NewsForm
import csv
import os

main_routes = Blueprint('main_routes', __name__)

@main_routes.route("/")
def index():
    return render_template("index.html")

@main_routes.route("/add_data", methods=["GET", "POST"])
def add_data():
    form = MarketDataForm()
    if form.validate_on_submit():
        date = form.date.data
        price = form.price.data
        volume = form.volume.data
        asset_type = form.asset_type.data
        HistoricalData.add_data(asset_type, date, price, volume)
        flash("Date adăugate cu succes!", "success")
        return redirect(url_for("main_routes.index"))
    return render_template("add_data.html", form=form)

@main_routes.route("/upload_csv", methods=["POST"])
def upload_csv():
    if 'file' not in request.files:
        flash("Niciun fișier selectat", "danger")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("Niciun fișier selectat", "danger")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        process_csv_file(filepath)
        flash("Datele din CSV au fost adăugate cu succes!", "success")
    return redirect(url_for("main_routes.index"))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_csv_file(filepath):
    with open(filepath, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip the header
        for row in csv_reader:
            asset_type, date, price, volume = row
            HistoricalData.add_data(asset_type, date, float(price), int(volume))

@main_routes.route("/add_instrument", methods=["GET", "POST"])
def add_instrument():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        Instrument.add_instrument(name, description)
        flash("Tip de activ adăugat cu succes!", "success")
        return redirect(url_for("main_routes.index"))
    return render_template("add_instrument.html")

@main_routes.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = form.news_content.data
        return redirect(url_for('main_routes.index'))
    return render_template('add_news.html', form=form)

