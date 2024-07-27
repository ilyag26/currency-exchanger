from db import *
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def error(error):
    return jsonify(
        massage = "Page not found"
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

@app.route('/exchange_rates', methods=['GET'])
def exchange_rates():
    Db1 = Db("currency.db")
    return jsonify(Db1.show_exchange()), 200

@app.route('/currency/<code>', methods=['GET'])
def currency_path(code):
    Db1 = Db("currency.db")
    return jsonify(Db1.show_currency_url(code)) if Db1.show_currency_url(code) else "Currency not exist", 200 if Db1.show_currency_url(code) else 404