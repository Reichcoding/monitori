import sqlite3
from datetime import datetime,timedelta
# connection = sqlite3.connect('pc_database.db')
# cursor = connection.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Pc (
# id INTEGER PRIMARY KEY NOT NULL,
# name TEXT NOT NULL,
# ip TEXT NOT NULL,
# ram_count INT NOT NULL,
# cpu_freq INT NOT NULL,
# description INT,
# disk_count INT NOT NULL,
# reg_data TEXT DEFAULT (strftime('%H:%M:%S %d.%m.%Y','now', 'localtime')) NOT NULL,
# has_battery INT NOT NULL


# )
# ''')

# connection.commit()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Data (
# id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# timestamp TEXT DEFAULT (strftime('%H:%M:%S %d.%m.%Y','now', 'localtime')) NOT NULL,
# pc_id INTEGER NOT NULL,
# cpu_load INTEGER NOT NULL,
# ram_load INTEGER NOT NULL,
# disk_load INTEGER NOT NULL,
# ram_load_gb INTEGER NOT NULL,
# disk_load_gb INTEGER NOT NULL,
# battery INTEGER

# )
# ''')

# connection.commit()


# from datetime import datetime,timedelta
for i in range(0,24):
    print(i)