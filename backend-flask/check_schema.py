import sqlite3

conn = sqlite3.connect('foodorder.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(restaurants)')
print('Restaurants columns:')
for row in cursor.fetchall():
    print(f'  {row[1]} ({row[2]})')
