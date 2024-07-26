from flask import Flask, request, jsonify
from waitress import serve
import sqlite3

class Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def show_currency(self):

        self.conn.row_factory = sqlite3.Row 
        users = self.cursor.execute("SELECT * FROM `Currencies`")
        return users.fetchall()

    # def add_records(self,user_id, user_balance):
    #     result = self.cursor.execute("UPDATE `currency` SET `user_balance` = ? WHERE `user_id` = ?",(user_balance,user_id))
    #     return self.conn.commit()
    
    def add_currency(self, code, fullname, sign):
        result = self.cursor.execute("INSERT INTO `Currencies` (`code`,`fullname`, `sign`) VALUES (?,?,?)",(code,fullname,sign))
        return self.conn.commit()

    # def show_records(self):
    #     users = self.cursor.execute("SELECT * FROM `records`")
    #     return users.fetchall()

    def close(self):
        self.conn.close()

app = Flask(__name__)

#http://localhost:8080/currency_add?code=USD&fullname=United%20States%20dollar&sign=$
@app.route('/currency_add', methods=['POST'])
def index():
    Db1 = Db("currency.db")
    code = request.args.get('code')
    fullname = request.args.get('fullname')
    sign = request.args.get('sign')
    Db1.add_currency(code,fullname,sign)
    return "Success", 200

#http://localhost:8080/currency
@app.route('/currency', methods=['POST'])
def currency():
    Db1 = Db("currency.db")
    ar = []
    for i in range(0, len(Db1.show_currency())):
        date = {
            "id" : Db1.show_currency()[i][0],
            "code" : Db1.show_currency()[i][1],
            "fullname" : Db1.show_currency()[i][2],
            "sign" : Db1.show_currency()[i][3]
        }
        ar.append(date)
    return jsonify(ar)

# for index in Db.show_users():
#     print(index)
# print("---------")
# for index in Db.show_records():
#     print(index)
# Db.add_user(3232321,32388383)
# Db.edit_user(3232321,999999999)
# Db.add_records(334827647, 987887)

serve(app, host="localhost", port=8080)