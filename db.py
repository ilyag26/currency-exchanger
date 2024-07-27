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

def formate_data_exchange(data):
    Db1 = Db("currency.db")
    ar = []
    for i in range(0, len(data)):
        date = {
            "Id" : data[i][0],
            "BaseCurrencyId" : Db1.show_currency_id(data[i][1]),
            "TargetCurrencyId" : Db1.show_currency_id(data[i][2]),
            "Rate" : data[i][3]
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
    
    def show_exchange(self):
        currency = self.cursor.execute(f"SELECT * FROM `ExchangeRates`")
        return formate_data_exchange(currency.fetchall())
    
    def show_currency_url(self, code):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies` WHERE code = ?", (code,))
        return formate_data(currency.fetchall())
    
    def show_currency_id(self, code):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies` WHERE id = ?", (code,))
        return formate_data(currency.fetchall())
    #   self.cursor.execute("UPDATE `currency` SET `user_balance` = ? WHERE `user_id` = ?",(user_balance,user_id))
    
    def add_currency(self, code, fullname, sign):
        result = self.cursor.execute("INSERT INTO `Currencies` (`code`,`fullname`, `sign`) VALUES (?,?,?)",(code,fullname,sign))
        return self.conn.commit()
    
    def add_currency_rate(self, id1, id2, rate):
        result = self.cursor.execute("INSERT INTO `ExchangeRates` (`basecurrencyid`,`targetcurrencyid`, `rate`) VALUES (?,?,?)",(id1,id2,rate))
        return self.conn.commit()
    
    def close(self):
        self.conn.close()