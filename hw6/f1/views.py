import requests
import json
from flask import request, jsonify, render_template

from app import app


currencies = requests.get('http://www.nbrb.by/API/ExRates/Currencies').json()
currencies_abv = (set(['BYN']) | set(item['Cur_Abbreviation'] for item in currencies)) - set(['RUR'])
DEFAULT_FROM = 'BYN'
DEFAULT_TO = 'USD'

with open('data.json', 'w') as f:
    json.dump(currencies, f)


@app.route('/')
def index():
    return render_template(
        'index.html',
        currencies=currencies_abv,
        default_from=DEFAULT_FROM,
        default_to=DEFAULT_TO
    )


@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    value = 0
    if data['to'] == 'BYN':
        cur = list(filter(lambda x: x['Cur_Abbreviation'] == data['from']['cur'], currencies))
        if cur:
            currency_id = cur[-1]['Cur_ID']
        r = requests.get(f'http://www.nbrb.by/API/ExRates/Rates/{currency_id}')
        if r.status_code == requests.codes.ok:
            cur_rate = r.json()
            rate = cur_rate['Cur_Scale'] / cur_rate['Cur_OfficialRate']
            value = round(data['from']['val'] / rate, 3)
    else:
        cur = list(filter(lambda x: x['Cur_Abbreviation'] == data['to'], currencies))
        if cur:
            currency_id = cur[-1]['Cur_ID']
        r = requests.get(f'http://www.nbrb.by/API/ExRates/Rates/{currency_id}')
        if r.status_code == requests.codes.ok:
            cur_rate = r.json()
            rate = cur_rate['Cur_Scale'] / cur_rate['Cur_OfficialRate']
            value = round(data['from']['val'] * rate, 3)
    return jsonify({'val': value})


@app.route('/refresh', methods=['POST'])
def refresh():
    global currencies
    print('Got refresh request')
    currencies = requests.get('http://www.nbrb.by/API/ExRates/Currencies').json()
    with open('data.json', 'w') as f:
        json.dump(currencies, f)
    return jsonify({})
