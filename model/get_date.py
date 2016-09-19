import os
import sys
import time
import datetime
import random

def get_date():
    date_time = time.strftime('%Y-%m-%d', time.localtime())
    date_now = datetime.datetime.strptime(date_time, "%Y-%m-%d")
    date_change = random.randint(1, 4)
    new_order_date = date_now + datetime.timedelta(days = date_change)
    new_order_date = new_order_date.strftime("%Y-%m-%d")
    return new_order_date