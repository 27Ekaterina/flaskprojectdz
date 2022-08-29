import sqlite3
from sqlite3 import connect

conn = sqlite3.connect('hhsqlite.sqlite')
cursor = conn.cursor()

query = 'select w.word, a.regioncode, wsch.name, s.name, ws.count, ws.sellary, ws.percent from wordskills ws, words w, area a, where_search wsch, skills s where ws.id_word = w.id and ws.id_area = a.id and ws.id_where_search = wsch.id and ws.id_skill = s.id'

cursor.execute(query)

print(cursor.fetchall())