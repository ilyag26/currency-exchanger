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

#part of url
url = "http://localhost:8080"

def get_data():
    req = requests.get(url+"/currency")
    json_form = req.json()
    req2 = requests.get(url+"/exchangeRates")
    json_form2 = req2.json()
    return json_form, json_form2

@app.route('/')
def index():
    json_form, json_form2 = get_data()
    return render_template('index.html', data = json_form, data2 = json_form2)

# rendering html template
@app.route('/currency_list_delete')
def list_currency_delete():
    #sending get request to get list of currencies
    req = requests.get(url+"/currency")
    json_form = req.json()
    return render_template('pages/currency-list.html', data = json_form)

# rendering html template
@app.route('/currency_list')
def list_currency():
    #sending get request to get list of currencies
    json_form, json_form2 = get_data()
    return render_template('index.html', data = json_form, data2 = json_form2, data_currency = json_form)

@app.route('/process_currency', methods=['POST'])
def add_currency_result():
    #getting url params from request
    code = request.form['code']
    fullname = request.form['fullname']
    sign = request.form['sign']
    #sending post request to add new currency to db
    req = requests.post(url+f"/currency_add?code={code}&fullname={fullname}&sign={sign}")
    json_form3 = req.json()
    #get data that need to display data in index
    json_form, json_form2 = get_data()
    if req.status_code == 200:
        code_mes = "success"
    else:
        code_mes = "error"
    return render_template('index.html', code_status_add = code_mes, 
                           data = json_form, data2 = json_form2, data3 = json_form3)

@app.route('/rate_list')
def show_rate():
    #sending get request to get list of exchange rates that exist
    req = requests.get(url+"/exchangeRates")
    json_form3 = req.json()
    json_form, json_form2 = get_data()
    return render_template('index.html', data = json_form, data2 = json_form2, data_rates = json_form3)

@app.route('/rate_list_delete')
def list_rate_delete():
    #sending get request to get list of rates
    req = requests.get(url+"/exchangeRates")
    json_form = req.json()
    return render_template('pages/rate-list.html', data = json_form)

@app.route('/add_rate')
def add_rate():
    #sending get request to get list of currencies
    req = requests.get(url+"/currency")
    json_form = req.json()
    return render_template('index.html', data = json_form)

@app.route('/process_rate', methods=['POST', 'GET'])
def add_rate_process():
    #getting url params from request
    id1 = request.form['id1']
    id2 = request.form['id2']
    rate = request.form['rate']
    #sending post request to add new pare
    requests.post(url+f"/exchangeRates?id1={id1}&id2={id2}&rate={rate}")
    #sending get request to get list of currencies
    req3 = requests.get(url+"/currency")
    json_form, json_form2 = get_data()
    if req3.status_code == 200:
        code_mes = "success"
    else:
        code_mes = "error"
    return render_template('index.html', code_status = code_mes, data = json_form, data2 = json_form2)


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
    req3 = requests.get(url+f"/exchange?from={fromPare}&to={toPare}&amount={amount}")
    json_form3 = req3.json()
    #sending request to get rate's list

    json_form, json_form2 = get_data()

    if req3.status_code == 200:
        code_mes = "success"
    else:
        code_mes = "error"
    return render_template('index.html', data = json_form, data2 = json_form2,
                           data3 = json_form3, data_rate = json_form3,
                            code1 = code_mes if amount != "0" else "error")

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
    requests.patch(url+f"/exchangeRate/{code}?rate={rate}")
    #sending request to get rate's list
    req = requests.get(url+"/currency")
    json_form = req.json()
    req2 = requests.get(url+"/exchangeRates")
    json_form2 = req2.json()
    if req.status_code == 200:
        code_mes = "success"
    else:
        code_mes = "error"
    return render_template('index.html', data = json_form, data2=json_form2, status_code = code_mes)

@app.route('/currency_delete')
def delete_currencies():
    id = request.args.get('id')    
    requests.delete(url+f"/delete_currency?id={id}")
    #sending get request to get list of currencies
    req = requests.get(url+"/currency")
    json_form = req.json()

    return render_template('pages/currency-list.html', data = json_form)

@app.route('/rate_delete')
def delete_rates():
    id = request.args.get('id')    
    requests.delete(url+f"/delete_rate?id={id}")
    #sending get request to get list of currencies
    req = requests.get(url+"/exchangeRates")
    json_form = req.json()

    return render_template('pages/rate-list.html', data = json_form)
