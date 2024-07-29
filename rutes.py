from db import *
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def error(error):
    return jsonify(
        message = "Page not found"
    ), 404

@app.route('/currency_add', methods=['POST'])
def currency_add():
    Db1 = Db("currency.db")
    code = request.args.get('code')
    fullname = request.args.get('fullname')
    sign = request.args.get('sign')
    Db1.add_currency(code,fullname,sign)
    return Db1.show_currency_url(code), 200

@app.route('/exchange_rates_add', methods=['POST'])
def exchange_rates_add():
    Db1 = Db("currency.db")
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    rate = request.args.get('rate')
    Db1.add_currency_rate(id1,id2,rate)
    return "Success", 200

@app.route('/currency', methods=['GET'])
def currency():
    Db1 = Db("currency.db")
    return jsonify(Db1.show_currency()), 200

@app.route('/exchange', methods=['GET'])
def exchange_rates():
    Db1 = Db("currency.db")
    return jsonify(Db1.show_exchange()), 200

@app.route('/currency/<code>', methods=['GET'])
def currency_path(code):
    Db1 = Db("currency.db")
    return jsonify(Db1.show_currency_url(code)) if Db1.show_currency_url(code) else error_show("Currency not exist"), 200 if Db1.show_currency_url(code) else 404

@app.route('/exchange/<code>', methods=['GET'])
def exchange_path(code):
    Db1 = Db("currency.db")
    print(len(code))
    if len(code) == 6:
        first_code = Db1.show_currency_id_code(code[0:3])
        second_code = Db1.show_currency_id_code(code[3:6])
        rate = Db1.show_exchange_pare_id(Db1.show_exchange_id(first_code,second_code))
    else:
        first_code = 0
        second_code = 0
        rate = 0
    return jsonify(
        formate_data_exchange(rate) if rate else error_show("This pares not existed")
    ), 200 if rate else 404