from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QSpinBox, QComboBox, QCheckBox, QFrame
import configurator


class SettingsProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки")

        layout = QVBoxLayout()

        # Виджет для ввода данных (1-10)
        interval_label = QLabel(f"Интервал обновления(в сек.)")
        layout.addWidget(interval_label)

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(10)
        self.spin_box.setValue(int(int(configurator.get_config("data","update"))/1000))
        self.spin_box.valueChanged.connect(self.on_spin_box_changed)
        layout.addWidget(self.spin_box)


        # hr line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)

        # Выпадающее меню
        theme_label = QLabel(f"Тема оформления")
        layout.addWidget(theme_label)
        self.comboBox = QComboBox()

        items = ['dark_amber.xml',
                'dark_blue.xml',
                'dark_cyan.xml',
                'dark_lightgreen.xml',
                'dark_pink.xml',
                'dark_purple.xml',
                'dark_red.xml',
                'dark_teal.xml',
                'dark_yellow.xml',
                'light_amber.xml',
                'light_blue.xml',
                'light_cyan.xml',
                'light_cyan_500.xml',
                'light_lightgreen.xml',
                'light_pink.xml',
                'light_purple.xml',
                'light_red.xml',
                'light_teal.xml',
                'light_yellow.xml']

        
        self.comboBox.addItems(items)
        self.comboBox.setCurrentIndex(items.index(configurator.get_config("interface","theme")))
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        layout.addWidget(self.comboBox)

        # Выпадающее меню
        hide_label = QLabel(f"При запуске:")
        layout.addWidget(hide_label)
        self.hide_combo = QComboBox()
        self.hide_combo.addItems(['Спрятать','Развернуть'])
        if configurator.get_config("prog","onclose") == "tray":
            self.hide_combo.setCurrentIndex(0)
        else:
            self.hide_combo.setCurrentIndex(1)
        self.hide_combo.currentIndexChanged.connect(self.on_hide_combo_changed)
        layout.addWidget(self.hide_combo)

        # Чекбокс
        self.push_onload = QCheckBox("Автозагрузка")
        self.push_onload.stateChanged.connect(self.on_checkbox_changed)
        if configurator.get_config("prog","autoload") == "1":
            self.push_onload.setChecked(True)
        layout.addWidget(self.push_onload)
        self.update = QLabel(f"Данные cохраняются \nв реальном времени\n\n Для применения необходим\n перезапуск приложения")
        layout.addWidget(self.update)

        self.setLayout(layout)

    def on_spin_box_changed(self, value):
        # Функция, вызываемая при изменении значения в QSpinBox
        configurator.config_edit("data","update",str(value*1000))

    def on_combobox_changed(self, index):
        configurator.config_edit("interface","theme",self.comboBox.currentText())

    def on_checkbox_changed(self, state):
        # Функция, вызываемая при изменении состояния чекбокса
        if state == 2:  # 2 - Qt.Checked, 0 - Qt.Unchecked
            configurator.config_edit("prog","autoload","1")
        else:
            configurator.config_edit("prog","autoload","0")

    def on_hide_combo_changed(self, index):
        if self.hide_combo.currentText() == "Спрятать":
            configurator.config_edit("prog","onclose","tray")
        else:
            configurator.config_edit("prog","onclose","show")
    