from flask import Flask, request, jsonify
from waitress import serve
import sqlite3

def formate_data(data):
    ar = []
    for i in range(0, len(data)):
        date = {
            "id" : data[i][0],
            "code" : data[i][1],
            "fullname" : data[i][2],
            "sign" : data[i][3]
        }
        ar.append(date)
    return ar

class Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def show_currency(self):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies`")
        return formate_data(currency.fetchall())
    
    def show_currency_url(self, code):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies` WHERE code = ?", (code,))
        return formate_data(currency.fetchall())
    
    #   self.cursor.execute("UPDATE `currency` SET `user_balance` = ? WHERE `user_id` = ?",(user_balance,user_id))
    
    def add_currency(self, code, fullname, sign):
        result = self.cursor.execute("INSERT INTO `Currencies` (`code`,`fullname`, `sign`) VALUES (?,?,?)",(code,fullname,sign))
        return self.conn.commit()

    def close(self):
        self.conn.close()

app = Flask(__name__)

@app.errorhandler(404)
def error(error):
    return "Page not found", 404

#http://localhost:8080/currency_add?code=USD&fullname=United%20States%20dollar&sign=$
@app.route('/currency_add', methods=['POST'])
def currency_add():
    Db1 = Db("currency.db")
    code = request.args.get('code')
    fullname = request.args.get('fullname')
    sign = request.args.get('sign')
    Db1.add_currency(code,fullname,sign)
    return Db1.show_currency_url(code), 200

#http://localhost:8080/currency
@app.route('/currency', methods=['GET'])
def currency():
    Db1 = Db("currency.db")
    return jsonify(Db1.show_currency()), 200

#http://localhost:8080/currency/EUR
@app.route('/currency/<code>', methods=['GET'])
def currency_path(code):
    Db1 = Db("currency.db")
    return jsonify(Db1.show_currency_url(code)) if Db1.show_currency_url(code) else "Currency not exist", 200 if Db1.show_currency_url(code) else 404


serve(app, host="localhost", port=8080)