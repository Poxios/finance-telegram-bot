import requests
from bs4 import BeautifulSoup as bs


def get_usd_exchange_rate():
    page = requests.get("https://finance.naver.com/marketindex/")
    soup = bs(page.text, "html.parser")

    exchange_value = soup.select(
        '#exchangeList > li.on > a.head.usd > div > span.value')[0].get_text()
    changed_value = soup.select(
        '#exchangeList > li.on > a.head.usd > div > span.change')[0].get_text()
    changed_prefix = soup.select(
        '#exchangeList > li.on > a.head.usd > div > span.blind')[0].get_text()
    icon = '🧨' if changed_prefix == '상승' else '🥶'
    return f'{exchange_value}원 [{changed_value.strip()} {changed_prefix}{icon}]\n'
