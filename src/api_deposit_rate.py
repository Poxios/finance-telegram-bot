from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('log-level=3')

c = DesiredCapabilities.CHROME
# To bypass page loading
c["pageLoadStrategy"] = "eager"


def get_highest_deposit_rate():
    try:
        # Remove `chromedriver` string if this is ubuntu env.
        driver = webdriver.Chrome(
            'chromedriver', options=options, desired_capabilities=c)
        driver.get('https://finlife.fss.or.kr/deposit/selectDeposit.do')
        sleep(1)
        # click '복리'
        driver.find_element(
            By.XPATH, '/html/body/div[2]/section[1]/div[2]/div[1]/div[3]/ul/li[3]/button').click()

        # click search
        driver.find_element(
            By.XPATH, '/html/body/div[2]/section[1]/div[2]/div[1]/button').click()

        sleep(1)

        highest_deposit_center = driver.find_element(
            By.XPATH, '/html/body/div[2]/section[1]/div[2]/div[2]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[2]').text
        highest_deposit_rate = driver.find_element(
            By.XPATH, '/html/body/div[2]/section[1]/div[2]/div[2]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[4]').text

        driver.quit()
        return f'{highest_deposit_center}: {highest_deposit_rate}\n'

    except Exception as e:
        return f'[DEPOSIT_ERROR] {e}'
