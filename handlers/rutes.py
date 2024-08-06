from db.database import *
from flask import Flask, request, jsonify

#init class class FLASK
app = Flask(__name__)
app.json.sort_keys = False

db_path="db/currency.db"

#showing error
@app.errorhandler(404)
def error(error):
    return jsonify(
        message = "Page not found"
    ), 404

#request to add new currency
@app.route('/currency_add', methods=['POST'])
def currency_add():
    Db1 = Db(db_path)
    code = request.args.get('code')
    fullname = request.args.get('fullname')
    sign = request.args.get('sign')
    Db1.add_currency(code,fullname,sign)
    return Db1.show_currency_url(code), 200

#request to create new exchange pare
@app.route('/exchangeRates', methods=['POST'])
def exchange_rates_add():
    Db1 = Db(db_path)
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    rate = request.args.get('rate')
    Db1.add_currency_rate(id1,id2,rate)
    return message_show("Success"), 200

#getting all currency that has database
@app.route('/currency', methods=['GET'])
def currency():
    Db1 = Db(db_path)
    return jsonify(Db1.show_currency()), 200

#getting all exchange pares that exist
@app.route('/exchangeRates', methods=['GET'])
def exchange_rates():
    Db1 = Db(db_path)
    return jsonify(Db1.show_exchange()), 200

#getting currency by code(EX: USD)
@app.route('/currency/<code>', methods=['GET'])
def currency_path(code):
    Db1 = Db(db_path)
    return jsonify(Db1.show_currency_url(code)) if Db1.show_currency_url(code) else message_show("Currency not exist"), 200 if Db1.show_currency_url(code) else 404

#request to show rate and pare exchange
@app.route('/exchangeRate/<code>', methods=['GET'])
def exchange_path(code):
    Db1 = Db(db_path)
    if len(code) == 6:
        first_code = Db1.show_currency_id_code(code[0:3])
        second_code = Db1.show_currency_id_code(code[3:6])
        #getting rate variable
        rate = Db1.show_exchange_pare_id(Db1.show_exchange_id(first_code,second_code))
    else:
        first_code = 0
        second_code = 0
        rate = 0
    return jsonify(
        formate_data_exchange(rate) if rate else message_show("This pares not existed")
    ), 200 if rate else 404

#request to change rate
@app.route('/exchangeRate/<code>', methods=['PATCH'])
def exchange_path_edit(code):
    Db1 = Db(db_path)
    rate = request.args.get('rate')
    #check if request has right length and if has rate
    if len(code) == 6 and rate:
        first_code = Db1.show_currency_id_code(code[0:3])
        second_code = Db1.show_currency_id_code(code[3:6])
        #check if exchange pare exist or no 
        if Db1.show_exchange_id(first_code,second_code):
            Db1.change_exchange_pare(rate,first_code,second_code)
        else:
            first_code = 0
            second_code = 0
    else:
        first_code = 0
        second_code = 0
    return message_show("Sucess") if first_code!=0 and second_code != 0 else message_show("Pare not exist"), 200 if rate else 404

#request to calculation of the transfer of a certain amount of funds from one currency to another
@app.route("/exchange", methods=["GET"])
def exchange_count():
    Db1 = Db(db_path)
    #getting requests params from request url
    base_code = request.args.get("from")
    target_code = request.args.get("to")
    amount = request.args.get("amount")
    #checking if params seted correctly
    if len(base_code) == 3 and len(target_code) == 3:
        #getting id in data base by code of currency
        base_id = Db1.show_currency_id_code(base_code)
        target_id = Db1.show_currency_id_code(target_code)
        #getting id pare exchange with function show_exchange_id
        pare_id = Db1.show_exchange_id(base_id,target_id)
        #checking if pare exist
        if pare_id:
            #getting rate amount from database by pare id
            rate = Db1.get_rate_value(pare_id)
            #deleting , from string to convert to float
            rate_changed = rate.replace(",", "")
            #counting converted amount
            converted_amount = float(amount)*float(rate_changed)/100
        else:
            rate = 0
    else:
        rate = 0
    return jsonify(
        formate_exchange_amount(Db1.show_exchange_pare_id(pare_id),amount,converted_amount)
        ) if rate != 0 else message_show("Pare not exist"), 200 if rate else 404
