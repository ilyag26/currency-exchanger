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
    #sending get request to get list of currencies
    req = requests.get("http://localhost:8080/currency")
    json_form = req.json()
    return render_template('pages/list_currency.html', data = json_form)


@app.route('/add_currency')
def add_currency():
    return render_template('pages/currency-add.html')


@app.route('/process_currency', methods=['POST'])
def add_currency_result():
    #getting url params from request
    code = request.form['code']
    fullname = request.form['fullname']
    sign = request.form['sign']
    #sending post request to add new currency to db
    requests.post(f"http://localhost:8080/currency_add?code={code}&fullname={fullname}&sign={sign}")
    return render_template('pages/currency-add.html', code1 = "success")


@app.route('/rate')
def show_rate():
    #sending get request to get list of exchange rates that exist
    req = requests.get("http://localhost:8080/exchangeRates")
    json_form = req.json()
    return render_template('pages/rate.html', data = json_form)

@app.route('/change_rate')
def change_rate():
    #sending get request to get list of exchange rates that exist
    req = requests.get("http://localhost:8080/exchangeRates")
    json_form = req.json()
    return render_template('pages/change-rate.html', data = json_form)

@app.route('/add_rate')
def add_rate():
    #sending get request to get list of currencies
    req = requests.get("http://localhost:8080/currency")
    json_form = req.json()
    return render_template('pages/rate-add.html', data = json_form)


@app.route('/process_rate', methods=['POST', 'GET'])
def add_rate_process():
    #getting url params from request
    id1 = request.form['id1']
    id2 = request.form['id2']
    rate = request.form['rate']
    #sending post request to add new pare
    requests.post(f"http://localhost:8080/exchangeRates?id1={id1}&id2={id2}&rate={rate}")
    #sending get request to get list of currencies
    req = requests.get("http://localhost:8080/currency")
    json_form = req.json()
    return render_template('pages/rate-add.html', code1 = "success", data=json_form)


@app.route('/make_exchange')
def exchange_route():
    #sending get request to get list of exchange rates
    req = requests.get("http://localhost:8080/exchangeRates")
    json_form = req.json()
    return render_template('pages/exchange-result.html', data = json_form)


@app.route("/exchange_detect", methods=["GET"])
def exchange_detect():
    db1 = Db(db_path)
    #getting params from first request from form
    pareId = request.args.get('pare_id')
    amount = request.args.get('amount')
    #getting dict with data with rate exchange by id (pareId)
    pareData = formate_data_exchange(db1.show_exchange_pare_id(pareId))
    #getting code base currency from recived dict
    for content in pareData:
        for content2 in content["baseCurrencyId"]:
            fromPare = content2["code"]
    #getting code target currency from recived dict
    for content in pareData:
        for content2 in content["targetCurrencyId"]:
            toPare = content2["code"]
    #sending new request with all data that we need too send request
    req = requests.get(f"http://localhost:8080/exchange?from={fromPare}&to={toPare}&amount={amount}")
    json_form = req.json()
    #sending request to get rate's list
    req2 = requests.get("http://localhost:8080/exchangeRates")
    json_form2 = req2.json()
    return render_template('pages/exchange-result.html', data = json_form2, data_rate = json_form, code1 = "success" if amount != "0" else "error")

@app.route('/change_rate_process')
def change_rate_process():
    db1 = Db(db_path)
    #get url params from request
    id = request.args.get('pare_id')
    rate = request.args.get('rate')
    #get id of base currency
    id_base = db1.get_id_base(id)[0]
    #get id of target currency
    id_target = db1.get_id_target(id)[0]
    #get code of target currency
    code_base = db1.get_code_currency(id_base)[0]
    #get code of target currency
    code_target = db1.get_code_currency(id_target)[0]
    #concatenate two code (EX: USD+EUR->USDEUR)
    code = str(code_base) + str(code_target)
    #sending request to change rate
    requests.patch(f"http://localhost:8080/exchangeRate/{code}?rate={rate}")
    #sending request to get rate's list
    req = requests.get("http://localhost:8080/exchangeRates")
    json_form = req.json()
    return render_template('pages/change-rate.html', data=json_form, code1 = "success")