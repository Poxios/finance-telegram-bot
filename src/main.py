from threading import Thread
from scheduler import Scheduler
import pytz
from time import sleep
from datetime import datetime as dt, timedelta, timezone, time

# Import from local
from api_stock import get_full_finance_info_message
from controller_sqlite import user_get_list
from controller_telegram import send_telegram_message, start_polling


# ! Scheduler
def schedule_checker(schedule):
    while True:
        schedule.exec_jobs()
        sleep(5)


def main():
    """ Send finance message to registered users """
    finance_message = get_full_finance_info_message()
    user_list_to_send = user_get_list()
    for user_id, user_name in user_list_to_send:
        msg_to_send = finance_message
        send_telegram_message(user_id, msg_to_send)

    print(f'[SCHEDULE] Success Running {dt.now()}')


if __name__ == "__main__":
    TZ_SEOUL = pytz.timezone('Asia/Seoul')
    schedule = Scheduler(tzinfo=TZ_SEOUL)
    trigger = time(hour=7, tzinfo=TZ_SEOUL)
    schedule.daily(trigger, main)
    print(schedule)

    # Start Scheduler
    Thread(target=lambda: schedule_checker(schedule)).start()

    # Start polling messages from telegram
    start_polling()
