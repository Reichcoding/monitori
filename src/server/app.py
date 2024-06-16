import sys
sys.path.append('modules/')

from flask import Flask,send_from_directory, render_template, session, request, redirect, url_for,flash
import configurator
import requests
import sqlite3
import time
import charts
import configparser
import datetime
import os


if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    application = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    application = Flask(__name__)

application.secret_key = configurator.get_config('app','secret_key')


computers = {}
pc_commands = {}


    
def registrate_pc(pc_id,data):
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Pc WHERE id = {pc_id}")
    pcs = cursor.fetchall()
    if len(pcs)>0:
        connection.close()
        return
    battery = 0
    if data['battery']!=False:
        battery = 1
    cursor.execute(f"INSERT INTO Pc (id,name,ip,ram_count,cpu_freq,disk_count,has_battery) VALUES({pc_id},'{data["pc_name"]}','{data["ip"]}','{data["ram_total"]}','{data["hertz"]}','{data["disk_total"]}','{battery}')")
    connection.commit()
    connection.close()



@application.route('/receive_data', methods=['POST'])
def data_receive():
    content = request.json
    pc_id = int(content["ip"].split(".")[0])+int(content["ip"].split(".")[1])+int(content["ip"].split(".")[3])+(int(content["ip"].split(".")[2])*255)
    registrate_pc(pc_id,content)
    computers[pc_id] = content
    if pc_commands.get(pc_id) != None:
        command = pc_commands.get(pc_id)
        pc_commands.pop(pc_id)
        return command
    return "received"


@application.route('/')
@application.route('/index')
def index():
    if session.get("access") == None:
        return redirect(url_for('login'))
    return render_template("index.html")


@application.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == configurator.get_config("access","password"):
            session['access'] = "true"
            return redirect(url_for('index'))
        flash("Неверный пароль")
        print("wrong")
    return render_template("login.html")


@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('access', None)
    return redirect(url_for('login'))


@application.route('/config')
def config():
    if session.get("access") == None:
        return redirect(url_for('login'))
    
    cfg = {}
    cfg["data_registration_speed"] = configurator.get_config("server","data_registration_speed")
    cfg["registrate_data"] = configurator.get_config("server","registrate_data")
    cfg["data_check_expire"] = configurator.get_config("server","data_check_expire")
    cfg["ip"] = configurator.get_config("server","ip")
    cfg["port"] = configurator.get_config("server","port")
    cfg["data_expire_rate"] = configurator.get_config("server","data_expire_rate")
    return render_template("settings.html", cfg=cfg)


@application.route('/change_pass', methods=['GET','POST'])
def change_settings():
    if session.get("access") == None:
        return redirect(url_for('login'))
    configurator.config_edit("access","password",request.form["password"])
    return redirect(url_for('config'))


@application.route('/change_settings', methods=['GET','POST'])
def change_pass():
    if session.get("access") == None:
        return redirect(url_for('login'))
    configurator.config_edit("server","data_registration_speed",request.form["data_registration_speed"])
    if request.form.get('registrate_data') != None:
        configurator.config_edit("server","registrate_data","1")
    else:
        configurator.config_edit("server","registrate_data","0")
    configurator.config_edit("server","data_check_expire",request.form["data_check_expire"])
    configurator.config_edit("server","data_expire_rate",request.form["data_expire_rate"])
    configurator.config_edit("server","ip",request.form["ip"])
    configurator.config_edit("server","port",request.form["port"])
    if request.form["secret_key"] != "":
        configurator.config_edit("app","secret_key",request.form["secret_key"])
    flash("Настройки применяться только после перезагрузки сервера")
    return redirect(url_for('config'))



@application.route('/get_pcs', methods=['GET','POST'])
def get_pcs():
    return computers

@application.route('/archive', methods=['GET'])
def archive():
    if session.get("access") == None:
        return redirect(url_for('login'))
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Pc")
    pcs = cursor.fetchall()
    connection.close()
    return render_template("archive.html",pcs=pcs)




@application.route('/pc_data_<id>', methods=['GET'])
def pc_data(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Data WHERE pc_id={id} ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.execute(f"SELECT * FROM Pc WHERE id={id}")
    info = cursor.fetchone()
    connection.close()

    chart_cpu = charts.get_last_24h_avg(id,"cpu_load")
    chart_ram = charts.get_last_24h_avg(id,"ram_load")
    chart_disk = charts.get_last_24h_avg(id,"disk_load")

    dates = charts.get_min_max_day(id)

    return render_template("pc_data.html",info=info,data=data,chcpu=chart_cpu,chram=chart_ram,chdisk=chart_disk,max_date=dates[0],min_date=dates[1])


@application.route('/update_charts_<id>', methods=['POST'])
def update_charts(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    date = request.get_json()["date"]
    chart_cpu = charts.get_avg_by_date(id,"cpu_load",date)
    chart_ram = charts.get_avg_by_date(id,"ram_load",date)
    chart_disk = charts.get_avg_by_date(id,"disk_load",date)

    return {"cpu":chart_cpu,"ram":chart_ram,"disk":chart_disk}


@application.route('/total_chart_<id>', methods=['POST'])
def update_total_charts(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    date1 = request.get_json()["min_date"]
    date2 = request.get_json()["max_date"]
    chart_cpu = charts.get_avg_by_date_to_date(id,"cpu_load",date1,date2)
    chart_ram = charts.get_avg_by_date_to_date(id,"ram_load",date1,date2)
    chart_disk = charts.get_avg_by_date_to_date(id,"disk_load",date1,date2)

    return {"cpu":chart_cpu,"ram":chart_ram,"disk":chart_disk}

 
@application.route('/describe_pc_<id>', methods=['GET','POST'])
def pc_describe(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    new_name = request.form["name"]
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Pc SET description='{new_name}' WHERE id='{id}'")
    connection.commit()
    connection.close()
    return redirect(f'pc_data_{id}')

@application.route('/delete_pc_<id>', methods=['GET','POST'])
def delete_pc(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    delete_pc(id)
    print(f"delete test '{id}'")
    return redirect(f'archive')


@application.route('/turn_off_pc_<id>', methods=['GET','POST'])
def turn_off_pc(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    if computers.get(int(id)) != None:
        pc_commands[int(id)] = "turnoff"
        flash("Команда отправлена.")
    else:
        flash("Команда не отправлена.")
    return redirect(f'/pc_data_{id}')

@application.route('/restart_pc_<id>', methods=['GET','POST'])
def restart_pc(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    if computers.get(int(id)) != None:
        pc_commands[int(id)] = "restart"
        flash("Команда отправлена.")
    else:
        flash("Команда не отправлена.")
    return redirect(f'/pc_data_{id}')

@application.route('/send_message_pc_<id>', methods=['GET','POST'])
def send_message_pc(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    if computers.get(int(id)) != None:
        pc_commands[int(id)] = f"show_message:{request.form["msg"]}"
        flash("Сообщение отправлено.")
    else:
        flash("Сообщение не отправлено.")
    return redirect(f'/pc_data_{id}')

@application.route('/send_command_pc_<id>', methods=['GET','POST'])
def send_command_pc(id):
    if session.get("access") == None:
        return redirect(url_for('login'))
    if computers.get(int(id)) != None:
        pc_commands[int(id)] = f"cmd:{request.form["cmd"]}"
        flash("Команда консоли отправлена.")
    else:
        flash("Команда консоли не отправлена.")
    return redirect(f'/pc_data_{id}')

@application.route('/retour', methods=['POST'])
def retour():
    if session.get("access") == None:
        return redirect(url_for('login'))
    # 
    token = "7113927501:AAE3udirHU0OFo-TcvzxugWw5ytFsg2NnQQ"
    id = 689567925
    message = f"WEB INTERFACE\n--------\n{request.form["email"]}\n-------------\n{request.form["text"]}"
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={message}")
    return redirect(f'index')


@application.route('/favicon.ico')
def favicon():
    return send_from_directory('static/imgs','favicon.ico', mimetype='image/vnd.microsoft.icon')

def check_computers_expiry():
    current_time = time.time()
    to_remove = []
    for computer in computers:
        if current_time - computers[computer]['timestamp'] > int(configurator.get_config('server','data_expire_rate')):
            print(f"{computer} dead")
            to_remove.append(computer)
    for i in to_remove:
        computers.pop(i)

def registrate_data():
    if int(configurator.get_config("server","registrate_data")) == 1:
        connection = sqlite3.connect('pc_database.db')
        cursor = connection.cursor()
        for pc in computers:
            if computers[pc]['battery'] !=False:
                cursor.execute(f"INSERT INTO Data (pc_id,cpu_load,ram_load,disk_load,ram_load_gb,disk_load_gb,battery) VALUES ({pc},{computers[pc]['cpu_use_perc']},{computers[pc]['ram_use_perc']},{computers[pc]['disk_use_perc']},{computers[pc]['ram_use_gb']},{computers[pc]['disk_use_gb']},{computers[pc]['battery']})")
            else:
                cursor.execute(f"INSERT INTO Data (pc_id,cpu_load,ram_load,disk_load,ram_load_gb,disk_load_gb) VALUES ({pc},{computers[pc]['cpu_use_perc']},{computers[pc]['ram_use_perc']},{computers[pc]['disk_use_perc']},{computers[pc]['ram_use_gb']},{computers[pc]['disk_use_gb']})")
        connection.commit()
        connection.close()

def delete_pc(pc_id):
    connection = sqlite3.connect('pc_database.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE from Data WHERE id={pc_id}")
    connection.commit()
    cursor.execute(f"DELETE from Pc WHERE id={pc_id}")
    connection.commit()
    connection.close()


import threading

def periodic_check():
    while True:
        check_computers_expiry()
        time.sleep(int(configurator.get_config('server','data_check_expire')))


def periodic_data_registrate():
    while True:
        registrate_data()
        time.sleep(int(configurator.get_config('server','data_registration_speed')))


t = threading.Thread(target=periodic_check)
t.daemon = True
t.start()
reg = threading.Thread(target=periodic_data_registrate)
reg.daemon = True
reg.start()


if __name__ == "__main__":
   application.run(host=configurator.get_config('server','ip'),port=int(configurator.get_config('server','port')))