import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('log-level=3')
options.page_load_strategy = 'eager'


def get_running_env_from_secret():
    with open('./src/secrets.json', 'r') as file:
        data = json.load(file)
        return data['RUNNING_OS']


def get_highest_deposit_rate():
    try:
        # Remove `chromedriver` string if this is ubuntu env.
        driver = None
        RUNNING_ENV = get_running_env_from_secret()
        if RUNNING_ENV == 'Windows':
            driver = webdriver.Chrome('chromedriver', options=options)
        else:
            driver = webdriver.Chrome(options=options)

        driver.get('https://finlife.fss.or.kr/finlife/svings/fdrmDpst/list.do?menuNo=700002')
        sleep(1)
        # # click '복리'
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/main/div[2]/div[1]/div[3]/dl/dd/div/div[3]').click()

        # # click search
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/main/div[2]/div[1]/div[8]/div/button[1]').click()

        sleep(1)

        highest_deposit_center = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/main/div[2]/div[8]/table/tbody/tr[1]/td[3]').text
        
        highest_deposit_rate = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/main/div[2]/div[8]/table/tbody/tr[1]/td[4]').text

        driver.quit()
        return f'{highest_deposit_center}: {highest_deposit_rate}\n'

    except Exception as e:
        print(e)
        return f'[DEPOSIT_ERROR]'

def test():
    print(get_highest_deposit_rate())

test()