from flask import Flask
from binance.client import Client
import config
from flask import jsonify, render_template
from itertools import groupby
import pandas as pd
import xlsxwriter
from decimal import *
from operator import itemgetter
from functools import cmp_to_key
from collections import OrderedDict
import simplejson as json


client = Client(config.api_key, config.api_secret)
app = Flask(__name__)


def get_all_tickers():
    return client.get_all_tickers()


def create_grouped_token_list(prices):
    # get all token who are in  ETH, BTC, BNB
    tokens_list = []
    check_list = ['ETH', 'BTC', 'BNB']
    exclude_list = ['ETHBTC', 'BNBBTC']
    for i in prices:
        if i['symbol'][-3:] in check_list and i['symbol'] not in exclude_list:
            tokens_list.append(i)
    grouped_symbols_list = []
    # group token on the basis of symbol
    for k, v in groupby(tokens_list, key=lambda x: x['symbol'][0:-3]):
        test_dict = {}
        for obj in list(v):
            test_dict[obj['symbol']] = obj['price']
        grouped_symbols_list.append(test_dict)
    grouped_symbols_list = sorted(grouped_symbols_list, key=lambda x: len(x))
    return grouped_symbols_list


def calc_arbitrage():
    prices = get_all_tickers()
    for data in prices:
        if data['symbol'] in ['ETHBTC', 'BNBBTC']:
            if data['symbol'] == 'ETHBTC':
                ETHBTC = data['price']
            else:
                BNBBTC = data['price']
    grouped_symbols_list = create_grouped_token_list(prices)
    final = []
    for obj in sorted(grouped_symbols_list, key=lambda x: len(x)):
        key_list = [x[-3:] for x in list(obj.keys())]
        if len(obj) >= 2 and (key_list == ['BTC', 'ETH'] or key_list == ['BTC', 'BNB'] or key_list == ['BTC', 'ETH', 'BNB']):
            for k, v in obj.items():
                if k[-3:] == 'BTC':
                    btc_base = Decimal(v)
                elif k[-3:] == 'ETH':
                    test_dict_1 = {}
                    eth_btc_equiv = Decimal(ETHBTC) * Decimal(v)
                    ETH_ARBITRAGE = round(
                        ((btc_base - eth_btc_equiv)/btc_base*100), 2
                    )
                    test_dict_1['token'] = k
                    test_dict_1['BTC'] = btc_base
                    test_dict_1['BTC_EQUIV'] = eth_btc_equiv
                    test_dict_1['ARBITRAGE'] = ETH_ARBITRAGE
                    final.append(test_dict_1)

                else:
                    test_dict_2 = {}
                    bnb_btc_equiv = Decimal(BNBBTC) * Decimal(v)
                    BNB_ARBITRAGE = round(
                        ((btc_base - bnb_btc_equiv)/btc_base*100), 2
                    )
                    test_dict_2['token'] = k
                    test_dict_2['BTC'] = btc_base
                    test_dict_2['BTC_EQUIV'] = bnb_btc_equiv
                    test_dict_2['ARBITRAGE'] = BNB_ARBITRAGE
                    final.append(test_dict_2)
    response = sorted(final, key=itemgetter('ARBITRAGE'), reverse=True)
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ajax-table/', methods=['POST'])
def ajax_table_data():
    response = calc_arbitrage()
    final = {'draw': "", "recordsTotal": "", "recordsFiltered": "", "data": ""}
    final['draw'] = 1
    final['data'] = response
    final['recordsTotal'] = len(response)
    final['recordsFiltered'] = len(response)
    return json.dumps(final)
