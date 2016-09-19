import sqlite3
import os
import sys

Users_db = sqlite3.connect("web_database.db")
Users_cu = Users_db.cursor()

def create_table():
    if not Users_cu.execute('SELECT count(*) FROM sqlite_master Where type="table" AND name="Stations_table"').fetchone()[0]:
        Users_cu.execute('CREATE TABLE Stations_table(station_name TEXT, lng DOUBLE, lat DOUBLE, count_number_plan DOUBLE, count_number_real DOUBLE)')

