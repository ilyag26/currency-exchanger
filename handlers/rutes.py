from db.database import *
from flask import Flask, request, jsonify

#init class class FLASK
app = Flask(__name__)

#showing error
@app.errorhandler(404)
def error(error):
    return jsonify(
        message = "Page not found"
    ), 404

#request to add new currency
@app.route('/currency_add', methods=['POST'])
def currency_add():
    Db1 = Db("currency.db")
    code = request.args.get('code')
    fullname = request.args.get('fullname')
    sign = request.args.get('sign')
    Db1.add_currency(code,fullname,sign)
    return Db1.show_currency_url(code), 200

#request to create new exchange pare
@app.route('/exchangeRates', methods=['POST'])
def exchange_rates_add():
    Db1 = Db("currency.db")
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    rate = request.args.get('rate')
    Db1.add_currency_rate(id1,id2,rate)
    return "Success", 200

#getting all currency that has database
@app.route('/currency', methods=['GET'])
def currency():
    Db1 = Db("currency.db")
    return jsonify(Db1.show_currency()), 200

#getting all exchange pares that exist
@app.route('/exchangeRates', methods=['GET'])
def exchange_rates():
    Db1 = Db("currency.db")
    return jsonify(Db1.show_exchange()), 200

#getting currency by code(EX: USD)
@app.route('/currency/<code>', methods=['GET'])
def currency_path(code):
    Db1 = Db("currency.db")
    return jsonify(Db1.show_currency_url(code)) if Db1.show_currency_url(code) else message_show("Currency not exist"), 200 if Db1.show_currency_url(code) else 404

#request to show rate and pare exchange
@app.route('/exchangeRate/<code>', methods=['GET'])
def exchange_path(code):
    Db1 = Db("currency.db")
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
    Db1 = Db("currency.db")
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