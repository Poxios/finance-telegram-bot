import requests
from dateutil import parser
import json
from datetime import datetime as dt, timedelta
import talib
import yfinance as yf


def __get_stock_price_and_rsi(stock_name: str) -> str:
    # Start fetching from 6 months ago to calculate the rsi.
    start_date = (dt.today() - timedelta(days=93)).strftime("%Y-%m-%d")
    data = yf.download(stock_name, start=start_date)
    stock_close_data = data['Close']
    rsi = talib.RSI(stock_close_data)

    last_date = stock_close_data.index[-1].date()
    last_close_value = stock_close_data[-1]
    prev_close_value = stock_close_data[-2]

    # Formatting Stock Name
    stock_name_str = "{0: <5}".format(stock_name)

    # Icon
    icon_prefix = '🧨'if last_close_value > prev_close_value else '🥶'

    # Last Close Value
    last_close_value_str = "{0: <7}".format(round(last_close_value, 3))

    # Rise Rate
    rise_or_down_prefix = '+'if last_close_value > prev_close_value else ''
    rise_rate_str = f'({rise_or_down_prefix}{round((last_close_value - prev_close_value)/prev_close_value*100,2)}%)'

    # RSI Rate
    fetched_rsi_value = round(rsi.iat[-1], 2)
    rsi_str = f'[RSI {fetched_rsi_value}]'

    return f'{stock_name_str}{icon_prefix}{last_close_value_str}{rise_rate_str} {rsi_str}'


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
            return f'({prefix}{round(today-prev,2)}){icon}'

        return f'<{round(data["score"],2)}> {data["rating"].capitalize()} [{data_time.date()}]\n' +\
            f'Before 1D: {round(data["previous_close"],2)}{gap_between_prev(data["score"],data["previous_close"])}\n' +\
            f'Before 1W: {round(data["previous_1_week"],2)}{gap_between_prev(data["score"],data["previous_1_week"])}\n' +\
            f'Before 1M: {round(data["previous_1_month"],2)}{gap_between_prev(data["score"],data["previous_1_month"])}\n'

    else:
        return f'FearAndGreed value failed to fetch. Status Code: {response.status_code}\n'


def get_full_finance_info_message():
    print('[MESSAGE] Fetching finance info..')
    response_str = dt.date()

    response_str += '---Stock Info---\n'
    for ticker in ['QQQ', 'IVV']:
        response_str += (__get_stock_price_and_rsi(ticker)+'\n')

    response_str += '\n---Fear And Greed---\n'
    response_str += __get_fear_and_greed_value()

    response_str += '\n---Exchange Rate---\n'
    response_str += 'TODO\n'

    response_str += '\n---Deposit Rate---\n'
    response_str += 'TODO\n'

    return response_str
