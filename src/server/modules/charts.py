import sqlite3
from datetime import datetime,timedelta

def get_last_24h_avg(pc_id,chart):
    return_data = []
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    for i in range(0,24):
        now = datetime.now() - timedelta(hours=i)
        hour = now.strftime('%H')
        date = now.strftime('%d.%m.%Y')
        cursor.execute(f"SELECT AVG({chart}) FROM Data WHERE timestamp LIKE '{hour}:__:__ {date}' AND pc_id='{pc_id}' ")
        data = cursor.fetchall()
        for j in data:
            dt = j[0]
            if dt == None:
                dt = 0
            return_data.append([f"{hour}:00",f"{round(dt,2)}"])
    connection.close()
    return_data.reverse()
    return return_data

def get_avg_by_date(pc_id,chart,date):
    return_data = []
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    for i in range(23,0,-1):
        cursor.execute(f"SELECT AVG({chart}) FROM Data WHERE timestamp LIKE '{i}:__:__ {date}' AND pc_id='{pc_id}' ")
        data = cursor.fetchall()
        for j in data:
            dt = j[0]
            if dt == None:
                dt = 0
            return_data.append({"time":f"{i}:00","load":f"{round(dt,2)}"})
    connection.close()
    return_data.reverse()
    return return_data

def get_avg_by_date_to_date(pc_id,chart,date1,date2):
    return_data = []
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()

    date1 = datetime.strptime(date1, '%d.%m.%Y')
    date2 = datetime.strptime(date2, '%d.%m.%Y')

    while date2 >= date1:
        date = date2.strftime('%d.%m.%Y')
        datePokaz = date2.strftime('%d.%m')
        date2 = date2 - timedelta(days=1)
        for i in range(23,0,-1):
            cursor.execute(f"SELECT AVG({chart}) FROM Data WHERE timestamp LIKE '{i}:__:__ {date}' AND pc_id='{pc_id}' ")
            data = cursor.fetchall()
            for j in data:
                dt = j[0]
                if dt != None:
                    return_data.append({"time":f"{i}ч. {datePokaz}","load":f"{round(dt,2)}"})
    connection.close()
    return_data.reverse()
    return return_data

def get_min_max_day(pc_id):
    return_data = []
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT timestamp FROM Data WHERE pc_id='{pc_id}' ORDER BY id DESC LIMIT 1")
    min_date = cursor.fetchone()
    min_date = min_date[0].split(" ")[1].split(".")
    min_date.reverse()
    min_date = "-".join(min_date)
    return_data.append(min_date)
    cursor.execute(f"SELECT timestamp FROM Data WHERE pc_id='{pc_id}' ORDER BY id LIMIT 1")
    max_date = cursor.fetchone()
    max_date = max_date[0].split(" ")[1].split(".")
    max_date.reverse()
    max_date = "-".join(max_date)
    return_data.append(max_date)
    return return_data

