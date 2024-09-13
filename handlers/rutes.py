import requests

from db.database import *
from flask import (Flask, request,
                   jsonify, render_template,
                   redirect)

# init class FLASK
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.json.sort_keys = False

# path to db
db_path = "db/currency.db"

@app.route('/')
def index():
    return render_template('index.html')

# rendering html template
@app.route('/currency_list')
def list_currency():
    req = requests.get("http://localhost:8080/currency")
    json_form = req.json()
    return render_template('list_currency.html', data = json_form)

@app.route('/add_currency')
def add_currency():
    return render_template('currency-add.html')

@app.route('/add_currency/<code>')
def add_currency_code(code):
    return render_template('currency-add.html', code1 = code)

@app.route('/rate')
def show_rate():
    req = requests.get("http://localhost:8080/exchangeRates")
    json_form = req.json()
    return render_template('rate.html', data = json_form)