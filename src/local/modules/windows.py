from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

def create_menu_bar(app,settings,apisettings,help_block,about_block):
    def show_settings(self):
        settings.show()

    def show_api(self):
        apisettings.show()

    def show_help(self):
        help_block.show()
    
    def show_about(self):
        about_block.show()

    def hide_in_tray(self):
        for widget in app.topLevelWidgets():
            widget.hide()

    menu_bar = QMenuBar()
# 
# 
# 
    file_menu = menu_bar.addMenu('Файл')
    # 
    open_settings_action = QAction('Настройки', app)
    open_settings_action.triggered.connect(show_settings)
    file_menu.addAction(open_settings_action)
    # 
    hide_tray_action = QAction('Скрыть в трее', app)
    hide_tray_action.triggered.connect(hide_in_tray)
    file_menu.addAction(hide_tray_action)
    # 
    exit_action = QAction('Выход', app)
    exit_action.triggered.connect(app.quit)
    file_menu.addAction(exit_action)
    # 

# 
# 
# 
    api_menu = menu_bar.addMenu('API')
    # 
    open_api_settings = QAction('Настройки', app)
    open_api_settings.triggered.connect(show_api)
    api_menu.addAction(open_api_settings)
# 
# 
# 
    help_menu = menu_bar.addMenu('Помощь')
    # 
    open_help_form = QAction('Обратная связь', app)
    open_help_form.triggered.connect(show_help)
    help_menu.addAction(open_help_form)
    # 
    about_click = QAction('О программе', app)
    about_click.triggered.connect(show_about)
    help_menu.addAction(about_click)

    return menu_bar