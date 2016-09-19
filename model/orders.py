import sqlite3
import os
import sys

orders_db = sqlite3.connect("web_database.db")
orders_cu = orders_db.cursor()