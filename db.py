import sqlite3

def error_show(msg):
    date = {
        "message" : msg
    }
    return date

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
            "BaseCurrencyId" : Db1.show_currency_by_id(data[i][1]),
            "TargetCurrencyId" : Db1.show_currency_by_id(data[i][2]),
            "Rate" : data[i][3]
        }
        ar.append(date)
    return ar

class Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def show_currency(self):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies` group by id")
        return formate_data(currency.fetchall())
    
    def show_exchange(self):
        currency = self.cursor.execute(f"SELECT * FROM `ExchangeRates`")
        return formate_data_exchange(currency.fetchall())
    
    def show_currency_url(self, code):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies` WHERE code = ?", (code,))
        return formate_data(currency.fetchall())
    
    def show_currency_by_id(self, code):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies` WHERE id = ?", (code,))
        return formate_data(currency.fetchall())
    
    def show_currency_id_code(self, code):
        currency = self.cursor.execute(f"SELECT id FROM `Currencies` WHERE code = ?", (code,))
        result = currency.fetchall()[0][0]
        return result
    
    def show_exchange_id(self, code_first, code_second):
        currency = self.cursor.execute(f"SELECT * FROM `ExchangeRates` WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (code_first,code_second,))
        pare = currency.fetchall()
        if len(pare):
            result = a[0][0]
        else:
            result = 0
        return result
    
    def show_exchange_pare_id(self, code):
        currency = self.cursor.execute(f"SELECT * FROM `ExchangeRates` WHERE id = ?", (code,))
        return currency.fetchall()
    
    def add_currency(self, code, fullname, sign):
        result = self.cursor.execute("INSERT INTO `Currencies` (`code`,`fullname`, `sign`) VALUES (?,?,?)",(code,fullname,sign))
        return self.conn.commit()
    
    def add_currency_rate(self, id1, id2, rate):
        result = self.cursor.execute("INSERT INTO `ExchangeRates` (`basecurrencyid`,`targetcurrencyid`, `rate`) VALUES (?,?,?)",(id1,id2,rate))
        return self.conn.commit()
    
    def show_exchange_pare(self, code):
        currency = self.cursor.execute(f"SELECT * FROM `Currencies` WHERE id = ?", (code,))
        return self.conn.commit()
    
    def close(self):
        self.conn.close()