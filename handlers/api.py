from handlers.rutes import *

# showing error
@app.errorhandler(404)
def error():
    return jsonify(
        message = "Page not found"
    ), 404


# request to add new currency
@app.route('/currency_add', methods=['POST'])
def currency_add():
    db1 = Db(db_path)
    #getting request params
    code = request.args.get('code')
    fullname = request.args.get('fullname')
    sign = request.args.get('sign')
    db1.add_currency(code, fullname, sign)
    return jsonify(db1.show_currency_url(code)), 200


# request to create new exchange pare
@app.route('/exchangeRates', methods=['POST'])
def exchange_rates_add():
    db1 = Db(db_path)
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    rate = request.args.get('rate')
    db1.add_currency_rate(id1, id2, rate)
    return message_show("Success"), 200


# getting all currency that has database
@app.route('/currency', methods=['GET'])
def currency():
    db1 = Db(db_path)
    return jsonify(db1.show_currency())


# getting all exchange pares that exist
@app.route('/exchangeRates', methods=['GET'])
def exchange_rates():
    db1 = Db(db_path)
    return jsonify(db1.show_exchange()), 200


# getting currency by code(EX: USD)
@app.route('/currency/<code>', methods=['GET'])
def currency_path(code):
    db1 = Db(db_path)
    return jsonify(db1.show_currency_url(code)) if db1.show_currency_url(code) else message_show("Currency not exist"), 200 if db1.show_currency_url(code) else 404


# request to show rate and pare exchange
@app.route('/exchangeRate/<code>', methods=['GET'])
def exchange_path(code):
    Db1 = Db(db_path)
    if len(code) == 6:
        #splitting code from request
        first_code = Db1.show_currency_id_code(code[0:3])
        second_code = Db1.show_currency_id_code(code[3:6])
        # getting rate variable
        rate = Db1.show_exchange_pare_id(Db1.show_exchange_id(first_code,second_code))
    else:
        first_code = 0
        second_code = 0
        rate = 0
    return jsonify(
        formate_data_exchange(rate) if rate else message_show("This pares not existed")
    ), 200 if rate else 404


# request to change rate
@app.route('/exchangeRate/<code>', methods=['PATCH'])
def exchange_path_edit(code):
    db1 = Db(db_path)
    rate = request.args.get('rate')
    # check if request has right length and if has rate
    if len(code) == 6 and rate:
        #getting first and second code from request url
        first_code = db1.show_currency_id_code(code[0:3])
        second_code = db1.show_currency_id_code(code[3:6])
        # check if exchange pare exist or no
        if db1.show_exchange_id(first_code, second_code):
            db1.change_exchange_pare(rate, first_code, second_code)
        else:
            first_code = 0
            second_code = 0
    else:
        first_code = 0
        second_code = 0
    return message_show("Sucess") if first_code != 0 and second_code != 0 else message_show("Pare not exist"), 200 if rate else 404


# request to calculation of the transfer of a certain amount of funds from one currency to another
@app.route("/exchange", methods=["GET"])
def exchange_count():
    db1 = Db(db_path)
    # getting requests params from request url
    base_code = request.args.get('from')
    target_code = request.args.get('to')
    amount = request.args.get('amount')
    # checking if params seted correctly
    if len(base_code) == 3 and len(target_code) == 3:
        # getting id in data base by code of currency
        base_id = db1.show_currency_id_code(base_code)
        target_id = db1.show_currency_id_code(target_code)
        # getting id pare exchange with function show_exchange_id
        pare_id = db1.show_exchange_id(base_id,target_id)
        # checking if pare exist
        if pare_id:
            # getting rate amount from database by pare id
            rate = db1.get_rate_value(pare_id)
            # counting converted amount
            converted_amount = float(amount)*float(rate)
        else:
            rate = 0
    else:
        rate = 0
    return jsonify(
        formate_exchange_amount(db1.show_exchange_pare_id(pare_id),amount,converted_amount)
        ) if rate != 0 else message_show("Pare not exist"), 200 if rate else 404