import sys
sys.path.append('modules/')

import socket
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow, QLabel, QProgressBar,QFrame, QSystemTrayIcon, QMenu, QStyle
from PyQt6.QtCore import QTimer, pyqtSlot, pyqtSignal, QThread
from PyQt6.QtGui import QAction,QIcon
import time
import os
from qt_material import apply_stylesheet
import sensors
import requests,json
import cpu_window
import windows
import disk_window
import configurator
import settings_program,settings_api,help_form_window,about_window
import threading 
import processlist

import psutil,configparser,gpiozero

from notifypy import Notify
class Sensors_Thread(QThread):
    data_updated = pyqtSignal(list)

    def run(self):
        timer = QTimer()
        timer.timeout.connect(self.get_sensor_data)
        timer.start(int(configurator.get_config("data","update")))

        self.host_name = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host_name)
        self.hertz = sensors.cpu_freq()

        reg = threading.Thread(target=self.send_data_server)
        reg.daemon = True
        reg.start()

        self.exec()
    def do_something(response):
        print(response.text)

    def send_data_server(self):
        while True:
            if configurator.get_config("api","onload") == "0":
                return #прерывание исполенения при выключенном подключении
            data = self.get_sensor_data(server=True)
            post_data = {
                "pc_name":self.host_name,
                "ip":self.ip_address,
                "cpu_use_perc":data[0],
                "ram_use_perc":data[1],
                "ram_use_gb":data[3],
                "ram_total":data[4],
                "disk_use_gb":data[5],
                "disk_total":data[6],
                "disk_use_perc":data[2],
                "battery":data[7],
                "hertz":self.hertz,
                "process":processlist.get_programs(),
                "timestamp":time.time()
            }
            url = f"http://{configurator.get_config("api","ip")}:{configurator.get_config("api","port")}/receive_data"
            try:
                r = requests.post(url, data=json.dumps(post_data),headers={'Content-type': 'application/json'})
                if r.status_code != 200:
                    return # завершение обработки при ошибке.
                if r.text == "received":
                    pass # пропуск 200 ответа
                elif r.text == "turnoff":
                    os.system("shutdown /f /s /t 0")
                    os.system("shutdown -h now")
                elif r.text == "restart":
                    os.system("shutdown /r /f /t 0")
                    os.system("reboot")
                elif r.text.split(":")[0] == "show_message":
                    notification = Notify()
                    notification.title = "Monitor Operator"
                    notification.message = f"{r.text.split(":")[1]}"
                    notification.icon = "logo.png"
                    notification.send()
                elif r.text.split(":")[0] == "cmd":
                    os.system(r.text.split(":")[1]) # исполнение переданной команды  
                else:
                    return
            except:
                pass
            time.sleep(int(configurator.get_config("api","update")))
    @pyqtSlot()
    def get_sensor_data(self,server=False):
        # Получение данных для вывода в основное меню
        cpu_percent = sensors.cpu_percent(True)
        ram_load = sensors.ram_using_percentage()
        ram_used = sensors.ram_data(True)
        ram_total = sensors.ram_data()
        disk_used = sensors.disk_get_all_disk_data(True)
        disk_total = sensors.disk_get_all_disk_data(False)
        disk_load = sensors.disk_get_all_using_percentage()

        battery_data = sensors.battery_percent()

        data = [cpu_percent,ram_load,disk_load,ram_used,ram_total,disk_used,disk_total,battery_data]
        
        # Если данные для сервера - возврат данных без вызова слота.
        if server:
            return data
        # Отправка данных в функцию обновления
        self.data_updated.emit(data)





class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        app.setWindowIcon(QIcon('icon.ico'))

        self.setWindowTitle('Main Page')
        layout = QVBoxLayout()

        # get sensors data
        self.sensor_thread = Sensors_Thread()
        self.sensor_thread.data_updated.connect(self.update_progress_bars)
        self.sensor_thread.start()

        # Массив прогрессбаров для дальнейшего обновления
        self.data_loads = []

        #
        # CPU ALLCORES LOAD
        # 
        #  

        self.core_label = QLabel(f"Загрузка процессора - 0 %")
        self.core_freq = QLabel(f"Частота - {sensors.cpu_freq()} MHz ")
        self.cpu_load_progress = QProgressBar()
        self.cpu_load_progress.setRange(0, 100)  # Диапазон значений для прогрессбара
        self.cpu_load_progress.setValue(0)
        layout.addWidget(self.core_label)
        layout.addWidget(self.core_freq)
        layout.addWidget(self.cpu_load_progress)
        self.data_loads.append(self.cpu_load_progress)
        # Кнопка подробнее
        button = QPushButton('Подробнее...')
        button.clicked.connect(self.open_allcores)
        layout.addWidget(button)

        # hr line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)


        #
        # RAM DATA
        # 
        #  
        self.ram_label = QLabel(f"Загрузка ОЗУ - 0 %")
        self.ram_using_label = QLabel("")
        self.ram_load_percent = QProgressBar()
        self.ram_load_percent.setRange(0, 100)  # Диапазон значений для прогрессбара
        self.ram_load_percent.setValue(0)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_using_label)
        layout.addWidget(self.ram_load_percent)
        
        self.data_loads.append(self.ram_load_percent)

        # hr line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)

        #
        # DISK DATA
        # 
        #  
        self.disk_label = QLabel(f"Загрузка дисков - 0 %")
        self.disk_using_label = QLabel("")
        self.disk_load_percent= QProgressBar()
        self.disk_load_percent.setRange(0, 100)  # Диапазон значений для прогрессбара
        self.disk_load_percent.setValue(0)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.disk_using_label)
        layout.addWidget(self.disk_load_percent)
        self.data_loads.append(self.disk_load_percent)
        # Кнопка подробнее
        disk_data_button = QPushButton('Подробнее...')
        disk_data_button.clicked.connect(self.open_disk_alldata)
        layout.addWidget(disk_data_button)

        # hr line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)


        #
        # IF HAS BATTERY, RETURN CHARGE
        # 
        #  
        self.has_battery = False
        if sensors.battery_percent() != False:
            self.has_battery = True
        self.battery_label = QLabel(f"Батарея - Нет")
        self.battery_load_percent= QProgressBar()
        self.battery_load_percent.setRange(0, 100)  # Диапазон значений для прогрессбара
        self.battery_load_percent.setValue(0)
        layout.addWidget(self.battery_label)
        layout.addWidget(self.battery_load_percent)
        self.data_loads.append(self.battery_load_percent)

        # hr line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)


        #
        # ip address
        # 
        #  
        ip_label = QLabel(f'IP: {self.get_ip_address()}')
        layout.addWidget(ip_label)

        self.setLayout(layout)
    def get_ip_address(self):
        try:
            # Получаем локальный IP-адрес компьютера
            ip_address = socket.gethostbyname(socket.gethostname())
            return ip_address
        except:
            return 'N/A'
    # Функция обновления данных и подписей
    @pyqtSlot(list)
    def update_progress_bars(self, data):
        self.cpu_load_progress.setValue(int(data[0]))
        self.core_label.setText(f"Загрузка процессора - {int(data[0])} %")
        self.ram_load_percent.setValue(int(data[1]))
        self.ram_label.setText(f"Загрузка ОЗУ - {int(data[1])} %")
        self.disk_load_percent.setValue(int(data[2]))
        self.disk_label.setText(f"Загрузка дисков - {int(data[2])} %")
        self.ram_using_label.setText(self.drawlabel(data[3],data[4]))
        self.disk_using_label.setText(self.drawlabel(data[5],data[6]))
        if self.has_battery:
            self.battery_load_percent.setValue(int(data[7]))
            self.battery_label.setText(f"Заряд батареи - {int(data[7])} %")

    # Функция открытия расширенных данных о цпу
    def open_allcores(self):
        allcores_page.show()

    # Функция открытия расширенных данных о дисках
    def open_disk_alldata(self):
        diskdata_page.show()
    
    # Вспомогательная функция для корректного отображения названий
    def drawlabel(self, used,volume):
        return f"{used}GB/{volume}GB"

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Получение всех доступных окон
    main_page = MainPage()
    allcores_page = cpu_window.AllCores()
    diskdata_page = disk_window.DiskData()

    # Определение окон для вывода через менюбар
    settingsform = settings_program.SettingsProgram()
    apiform = settings_api.SettingsApi()
    helpform = help_form_window.HelpForm()
    aboutform = about_window.About()


    # Вывод в трей определенной иконки
    tray_icon = QSystemTrayIcon(main_page)
    tray_icon.setIcon(main_page.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton))

    # Созданию менюбара
    # Для меню бара необходимо передать окна для их открытия
    menu_bar = windows.create_menu_bar(app,settingsform,apiform,helpform,aboutform)
    # Создание окна и выдача ему менюбара
    main_window = QMainWindow()
    main_window.setMenuBar(menu_bar)
    main_window.setCentralWidget(main_page)


    # Определение стилей
    apply_stylesheet(app, theme=configurator.get_config("interface","theme"))

    # Скрытие приложение если в конфиге выставлен скрытый запуск
    if configurator.get_config("prog","onclose") != "tray":
        main_window.show()
    
    # Создаем контекстное меню для трея
    menu = QMenu()
    show_action = QAction("Открыть", main_page)
    hide_action = QAction("Спрятать", main_page)
    close_action = QAction("Закрыть", main_page)
    # Подлючение функций
    show_action.triggered.connect(main_window.show)
    hide_action.triggered.connect(main_window.hide)
    close_action.triggered.connect(app.quit)
    # Вывод меню для трея
    menu.addAction(show_action)
    menu.addAction(hide_action)
    menu.addAction(close_action)
    # Подключение контестного меню трею
    tray_icon.setContextMenu(menu)

    # Отображаем иконку в системном лотке
    tray_icon.show()

    sys.exit(app.exec())