import sqlite3
import os
import sys

Users_db = sqlite3.connect("web_database.db")
Users_cu = Users_db.cursor()

def create_table():
    if not Users_cu.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name="Users_table"').fetchone()[0]:
        Users_cu.execute('CREATE TABLE Users_table(id INTEGER, name TEXT, Email TEXT, Drivecard TEXT,  passwd TEXT)')


def checkUsers(check_name, check_Email, pw=None):
    Users_cu.execute('SELECT * FROM Users_table')
    Users_data = Users_cu.fetchall()
    if not pw:
        for i in Users_data:
            if check_name == i[1] and check_Email == i[2]:
                return True
        return False
    else:
        for i in Users_data:
            if check_name == i[1] and check_Email == i[2]:
                if pw == i[4]:
                    return True
                else:
                    return False
        return False