# coding:utf-8
import sqlite3

sql_db = sqlite3.connect("web_database.db")
sql_cu = sql_db.cursor()

fake_names = ['lhl', 'zjh', 'lw', 'pll', 'wy', 'ygx', 'wxl', 'xzw', 'sly', 'cl', 'zsh', 'dly', 'zyf', 'yzj', 'yc', 'qxy', 'ymf', 'ssy', 'gyl', 'tys', 'ls', 'wmy']

for p in fake_names:
    p_email = p + "@" + p + ".com"
    sql_cu.execute('INSERT  INTO Fake_users_table VALUES ("%s", "%s", "12345678901")' %(p, p_email))
    sql_db.commit()