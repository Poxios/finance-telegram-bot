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
    icon = '๐งจ' if changed_prefix == '์์น' else '๐ฅถ'
    return f'{exchange_value}์ [{changed_value.strip()} {changed_prefix}{icon}]\n'
