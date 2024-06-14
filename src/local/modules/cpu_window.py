from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QProgressBar, QMainWindow, QMenu
from PyQt6.QtCore import QTimer, pyqtSlot, pyqtSignal, QThread

import sensors
import configurator

class SensorThread(QThread):
    data_updated = pyqtSignal(list)

    def run(self):
        timer = QTimer()
        timer.timeout.connect(self.get_sensor_data)
        timer.start(int(configurator.get_config("data","update")))
        self.exec()

    @pyqtSlot()
    def get_sensor_data(self):
        data = sensors.cpu_percent()
        self.data_updated.emit(data)

class AllCores(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Загрузка потоков процессора")
        self.layout = QGridLayout()
        self.sensor_thread = SensorThread()
        self.sensor_thread.data_updated.connect(self.update_progress_bars)
        self.sensor_thread.start()

        self.cpu_loads = []
        self.core_labels = []

        self.init_ui()

    def init_ui(self):
        row = 0
        # Перебор логических процессоров в компьютере
        for i, load in enumerate(sensors.cpu_percent()):
            # Генерация строки для вывода 
            core_label = QLabel(f"#{i+1} - 0%")
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)  # Диапазон значений для прогрессбара
            progress_bar.setValue(round(load))
            self.layout.addWidget(core_label, i, 0)
            self.layout.addWidget(progress_bar, i, 1)
            self.cpu_loads.append(progress_bar)
            self.core_labels.append(core_label)
            row+=1

        self.setLayout(self.layout)

    @pyqtSlot(list)
    def update_progress_bars(self, data):
        for i, load in enumerate(data):
            self.cpu_loads[i].setValue(round(load))
            self.core_labels[i].setText(f"#{i+1} - {round(load)}%")