from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar,QLabel
from PyQt6.QtCore import QTimer, pyqtSlot, pyqtSignal, QThread
import configurator
import sensors

class SensorThread(QThread):
    data_updated = pyqtSignal(list)

    def run(self):
        timer = QTimer()
        timer.timeout.connect(self.get_sensor_data)
        timer.start(int(configurator.get_config("data","update")))
        self.exec()

    @pyqtSlot()
    def get_sensor_data(self):
        data = []
        data_used = []
        data_volume = []
        for i in sensors.get_avaible_drives():
            data.append(sensors.disk_using_percentage(i))
            data_used.append(sensors.disk_data(i,True))
            data_volume.append(sensors.disk_data(i,False))
        self.data_updated.emit([data,data_used,data_volume])

class DiskData(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Дисковая информация')
        layout = QVBoxLayout()

        # get sensors data
        self.sensor_thread = SensorThread()
        self.sensor_thread.data_updated.connect(self.update_progress_bars)
        self.sensor_thread.start()

        self.disk_loads = []
        self.disk_labels= []
        for i in sensors.get_avaible_drives():
            label = QLabel(f"Диск: {i}://")
            label2 = QLabel(self.drawlabel(0,0))
            prbar= QProgressBar()
            prbar.setRange(0,100)
            prbar.setValue(0)
            layout.addWidget(label)
            layout.addWidget(label2)
            layout.addWidget(prbar)
            self.disk_loads.append(prbar)
            self.disk_labels.append(label2)


        self.setLayout(layout)
    
    def drawlabel(self, used,volume):
        return f"{used}GB/{volume}GB"
    
    @pyqtSlot(list)
    def update_progress_bars(self, data):
        for i, load in enumerate(data[0]):
            self.disk_loads[i].setValue(round(load))
        for i, load in enumerate(data[1]):
            using = load
            volume = data[2][i]
            self.disk_labels[i].setText(self.drawlabel(using,volume))
        