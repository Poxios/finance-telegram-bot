import requests
from dateutil import parser
import json
from datetime import datetime as dt, timedelta
import talib
import yfinance as yf
# from telegram.utils.helpers import escape_markdown
# Import from local
import api_exchange_rate
import api_deposit_rate
from utils import generate_text_bar_graph


def __get_stock_price_and_rsi(stock_name: str) -> str:
    # Start fetching from 6 months ago to calculate the rsi.
    start_date = (dt.today() - timedelta(days=93)).strftime("%Y-%m-%d")
    data = yf.download(stock_name, start=start_date)
    stock_close_data = data['Close']
    rsi = talib.RSI(stock_close_data)

    last_date = stock_close_data.index[-1].date()
    fetched_month = last_date.month
    fetched_day = last_date.day

    last_close_value = stock_close_data[-1]
    prev_close_value = stock_close_data[-2]

    # Formatting Stock Name
    stock_name_str = "{0: <5}".format(f'<pre>{stock_name}</pre>')

    # Icon
    icon_prefix = '🧨'if last_close_value > prev_close_value else '🥶'

    # Last Close Value
    last_close_value_str = "{0: <5}".format(round(last_close_value, 3))

    # Rise Rate
    rise_or_down_prefix = '+'if last_close_value > prev_close_value else ''
    rise_rate_str = f'({rise_or_down_prefix}{round((last_close_value - prev_close_value)/prev_close_value*100,2)}%)'

    # RSI Rate
    fetched_rsi_value = round(rsi.iat[-1], 2)
    rsi_str = f'[RSI {fetched_rsi_value}]'

    return f'{stock_name_str} {icon_prefix}{last_close_value_str}{rise_rate_str} {rsi_str} {fetched_month}-{fetched_day}\n   RSI: ' +\
        generate_text_bar_graph(9, 30, fetched_rsi_value, 70)


def __get_fear_and_greed_value() -> str:
    today_str = dt.today().strftime("%Y-%m-%d")
    cnn_fear_and_greed_url = f'https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{today_str}'
    response = requests.get(cnn_fear_and_greed_url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
    if response.status_code == 200:
        data = json.loads(response.text)['fear_and_greed']
        data_time = parser.parse(data["timestamp"])

        def gap_between_prev(today: float, prev: float) -> str:
            prefix = '+' if today > prev else ''
            icon = '🧨' if today > prev else '🥶'
            return f'<pre>({prefix}{round(today-prev,2)}){icon}</pre>'

        return (f'<b>[{round(data["score"],2)}]</b> | {data["rating"].capitalize()} <i>{data_time.date()}</i>\n') +\
            generate_text_bar_graph(15, 0, round(data["score"], 2), 100)+'\n' +\
            'Before <pre>1D</pre>: '+(f'{round(data["previous_close"],2)}{gap_between_prev(data["score"],data["previous_close"])}\n') +\
            'Before <pre>1W</pre>: '+(f'{round(data["previous_1_week"],2)}{gap_between_prev(data["score"],data["previous_1_week"])}\n') +\
            'Before <pre>1M</pre>: ' + \
            (f'{round(data["previous_1_month"],2)}{gap_between_prev(data["score"],data["previous_1_month"])}\n')

    else:
        return (f'FearAndGreed value failed to fetch. Status Code: {response.status_code}\n')


def get_full_finance_info_message():
    print(f'[MESSAGE] Fetching finance info.. {dt.now()}')
    response_str = (f'{dt.now()}\n\n')

    response_str += '<b>Stock Info</b>\n'
    for ticker in ['QQQ', 'IVV']:
        response_str += (__get_stock_price_and_rsi(ticker)+'\n')

    response_str += '\n<b>Fear And Greed</b>\n'
    response_str += (__get_fear_and_greed_value())

    response_str += '\n<b>Exchange Rate</b>\n'
    response_str += (api_exchange_rate.get_usd_exchange_rate())

    response_str += '\n<b>Highest Deposit Rate</b>\n'
    response_str += (
        api_deposit_rate.get_highest_deposit_rate())

    print(f'[MESSAGE] Fetching finance info DONE {dt.now()}')
    return response_str
