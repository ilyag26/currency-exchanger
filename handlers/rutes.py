import requests

from db.database import *
from flask import (Flask, request,
                   jsonify, render_template)

# init class FLASK
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.json.sort_keys = False

# path to db
db_path = "db/currency.db"


# rendering html template
@app.route('/')
def index():
    req = requests.get("http://localhost:8080/currency")
    json_form = req.json()
    return render_template('index.html', data = json_form)

# rendering html template
@app.route('/add_currency')
def add_currency():
    return render_template('currency-add.html')