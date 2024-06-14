from PyQt6.QtWidgets import QWidget, QVBoxLayout,QLabel,QTextEdit,QLineEdit,QPushButton
import requests
import configurator


class About(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('О программе')
        layout = QVBoxLayout()

        label_email = QLabel("Приложение Monitor Operator")
        layout.addWidget(label_email)

    
        label_contact = QLabel("""
Данное приложение разработано для помощи в 
контроле загрузки компонентов аппаратного
обеспечения извне.
                               
------------------------
                               
Изначально у доступа к настройкам API
пароля нет. Для того чтобы доступ был
по паролю, необходимо его изменить
в вышеуказанном окне.

------------------------
                               
Разработано в 2024 специально для
дипломного проекта в БПОУ ОО "ОКОТСиТ"
Автор: Иванов Егор Русланович
""")
        layout.addWidget(label_contact)

        self.setLayout(layout)
