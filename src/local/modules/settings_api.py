from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QCheckBox,QLabel,QSpinBox,QPushButton,QFrame
import configurator
from hashlib import md5

class SettingsApi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки подключения")

        self.layout = QVBoxLayout()
        # Текстовое поле ввода 1
        self.password_label = QLabel(f"Пароль доступа")
        
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
    
        self.password_button = QPushButton('Вход')
        self.password_button.clicked.connect(self.admin_password_input)
        
        
        


        #
        #
        # PASSWORD INPUT ENDS
        #

        # Текстовое поле ввода 1
        self.ip_label = QLabel(f"IP подключения")

        self.ip_input = QLineEdit()
        self.ip_input.textChanged.connect(self.on_ip_changed)
        self.ip_input.setText(configurator.get_config("api","ip"))

        # Текстовое поле ввода 2
        self.port_label = QLabel(f"Порт подключения")

        self.port_input = QLineEdit()
        self.port_input.textChanged.connect(self.on_port_changed)
        self.port_input.setText(configurator.get_config("api","port"))

        

        # Виджет для ввода данных (1-10)
        self.connect_interval_label = QLabel(f"Интервал отправки данных(в сек.)")

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(5)
        self.spin_box.setMaximum(20)
        self.spin_box.setValue(int(int(configurator.get_config("api","update"))/1000))
        self.spin_box.valueChanged.connect(self.on_spin_box_changed)

        # Чекбокс
        self.push_onload = QCheckBox("Подключение")
        self.push_onload.stateChanged.connect(self.on_checkbox_changed)
        if configurator.get_config("api","onload") == "1":
            self.push_onload.setChecked(True)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        

        # Текстовое поле ввода 2
        self.pass_label = QLabel(f"Пароль доступа к API настройкам")
        
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_button = QPushButton('Изменить')
        self.pass_button.clicked.connect(self.admin_password_change)


        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.HLine)

        self.block_button = QPushButton('Выход')
        self.block_button.clicked.connect(self.button_show_admn)
        self.update = QLabel(f"Данные cохраняются \nв реальном времени\n")




        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.password_button)
        self.layout.addWidget(self.block_button)
        self.layout.addWidget(self.line2)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.port_label)
        self.layout.addWidget(self.port_input)
        self.layout.addWidget(self.connect_interval_label)
        self.layout.addWidget(self.spin_box)
        self.layout.addWidget(self.push_onload)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.pass_label)
        self.layout.addWidget(self.pass_input)
        self.layout.addWidget(self.pass_button)
        self.layout.addWidget(self.update)
        

        self.setLayout(self.layout)


        if configurator.get_config("api","password") == "0":
            self.show_adm_layouts(False)
        else:
            self.show_adm_layouts(True)

        


    def on_ip_changed(self, text):
        # configurator.config_edit("api","onload","0")
        # self.push_onload.setChecked(False)
        configurator.config_edit("api","ip",text)

    def on_port_changed(self, text):
        # configurator.config_edit("api","onload","0")
        # self.push_onload.setChecked(False)
        configurator.config_edit("api","port",text)

    def on_checkbox_changed(self, state):
        # Функция, вызываемая при изменении состояния чекбокса
        if state == 2:  # 2 - Qt.Checked, 0 - Qt.Unchecked
            configurator.config_edit("api","onload","1")
        else:
            configurator.config_edit("api","onload","0")
    def on_spin_box_changed(self, value):
        # Функция, вызываемая при изменении значения в QSpinBox
        configurator.config_edit("api","update",str(value*1000))

    
    
    def show_adm_layouts(self,show=True):
        if show:
            self.password_label.show()
            self.password.show()
            self.password_button.show()
            self.ip_label.hide()
            self.ip_input.hide()
            self.port_label.hide()
            self.port_input.hide()
            self.pass_label.hide()
            self.pass_input.hide()
            self.connect_interval_label.hide()
            self.spin_box.hide()
            self.push_onload.hide()
            self.line.hide()
            self.pass_button.hide()
            self.line2.hide()
            self.block_button.hide()
            self.update.hide()
        else:
            self.password_label.hide()
            self.password.hide()
            self.password_button.hide()
            self.ip_label.show()
            self.ip_input.show()
            self.port_label.show()
            self.port_input.show()
            self.pass_label.show()
            self.pass_input.show()
            self.connect_interval_label.show()
            self.spin_box.show()
            self.push_onload.show()
            self.line.show()
            self.pass_button.show()
            self.line2.show()
            self.block_button.show()
            self.update.show()
        self.adjustSize()

   
    def admin_password_input(self):
        if md5(self.password.text().encode()).hexdigest() == configurator.get_config("api","password"):
            self.show_adm_layouts(False)
            self.password.clear()

    def admin_password_change(self):
        text = self.pass_input.text()
        configurator.config_edit("api","password",md5(text.encode()).hexdigest())
        self.show_adm_layouts(True)
    
    def button_show_admn(self):
        if configurator.get_config("api","password") != "0":
            self.show_adm_layouts(True)