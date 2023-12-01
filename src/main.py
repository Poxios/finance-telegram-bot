import json
from threading import Thread
import schedule
import pytz
from time import sleep
from datetime import datetime as dt, timedelta, timezone, time
import requests


# Import from local
from api_stock import get_full_finance_info_message
from controller_sqlite import user_get_list
from controller_telegram import send_telegram_message, start_polling


# ! Scheduler
# def schedule_checker(schedule):
#     while True:
#         schedule.exec_jobs()
#         sleep(5)


def main():
    """Send finance message to registered users"""
    for user_id, user_name in user_get_list():
        msg_to_send = get_full_finance_info_message(user_id)
        print(f"Sending finance info to {user_name}...")
        send_telegram_message(user_id, msg_to_send)

    print(f"[SCHEDULE] Success Running {dt.now()}")


def health_check():
    """send http healthy message to config url"""
    with open("./src/secrets.json", "r") as file:
        data = json.load(file)["HEALTH_CHECK_URL"]
        if data:
            requests.get(data)


if __name__ == "__main__":
    schedule.every().day.at("07:00").do(main)
    schedule.every(1).minutes.do(health_check)
    Thread(target=start_polling).start()

    start_polling()
    print('[SYSTEM] Start scheduler')
    while True:
        schedule.run_pending()
        sleep(1)

    # # Start Scheduler
    # Thread(target=lambda: schedule_checker(schedule)).start()

    # # Start polling messages from telegram
    
