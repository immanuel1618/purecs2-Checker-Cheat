import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsOpacityEffect
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from pypresence import Presence  # Для Discord Rich Presence
import win32api
import win32con

# Импортируем страницы
from programs import ProgramsPage
from steam import SteamPage
from other import OtherPage
from searchsteam import get_loginusers_vdf_path
#from usbwindow import USBPage





# Функция для проверки прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

# Функция для перезапуска скрипта с правами администратора
def run_as_admin():
    if sys.argv[-1] != 'asadmin':  # Если скрипт еще не был запущен с правами
        # Перезапуск с правами администратора
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join([sys.argv[0], 'asadmin']), None, 1)
        sys.exit()

# Проверка, если скрипт не запущен с правами, перезапускаем с ними
if not is_admin():
    run_as_admin()

def resource_path(relative_path):
    """Получаем абсолютный путь к ресурсу (для разных сборщиков и для AppData)."""
    try:
        # Проверка для PyInstaller (или других упаковщиков, которые используют _MEIPASS)
        base_path = sys._MEIPASS
    except Exception:
        # Если не _MEIPASS, используем текущую директорию или путь из AppData
        # Попробуем использовать AppData для хранения ресурсов, если не в режиме разработки
        app_data_path = os.path.join(os.getenv('APPDATA'), 'MyApp')  # Пример пути для AppData
        if not os.path.exists(app_data_path):
            os.makedirs(app_data_path)
        base_path = app_data_path

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("purecs2 CheckerCheat")
        self.setFixedSize(1200, 700)

        # Главное окно с горизонтальным разделением
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Устанавливаем фон
        background_path = resource_path("assets/fon.png")
        self.background_label = QLabel(central_widget)
        self.background_label.setPixmap(QPixmap(background_path))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 1200, 700)
        self.background_label.lower()  # Отправляем фон на задний план

        # Discord Rich Presence
        self.discord_client_id = "1348517808975118366"  
        self.discord_rpc = Presence(self.discord_client_id)
        self.discord_rpc.connect()
        self.discord_rpc.update(state="Using purecs2 CheckerCheat", details="Main Menu")

        # Левая панель (Навигация)
        self.nav_panel = QWidget()
        self.nav_panel.setFixedWidth(300)
        self.nav_panel.setStyleSheet("background: transparent;")  # Делаем панель прозрачной
        nav_layout = QVBoxLayout(self.nav_panel)

        # Логотип
        logo_path = resource_path("assets/logo.png")
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap(logo_path).scaled(125, 125, Qt.KeepAspectRatio))
        self.logo_label.setFixedSize(125, 125)  # Фиксируем размер логотипа
        self.logo_label.mouseReleaseEvent = self.site_link
        self.logo_label.setCursor(Qt.PointingHandCursor)

        # Создаем контейнер для логотипа с отступами
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.addWidget(self.logo_label)
        logo_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)  # Выравниваем влево и вверх

        nav_layout.addWidget(logo_container)

        # Кнопки меню
        self.buttons = []
        self.active_button = None
        menu_items = ["Программы", "Steam", "Другое"]
        for item in menu_items:
            btn = QPushButton(item)
            btn.setFixedSize(260, 50)  # 250px ширина, 50px высота
            btn.setStyleSheet("""
                color: white;
                background-color: rgba(44, 109, 177, 1);
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, b=btn, item=item: self.set_active_button(b, item))
            nav_layout.addWidget(btn)
            self.buttons.append(btn)

        # Контейнер для соцсетей
        social_container = QWidget()
        social_layout = QHBoxLayout(social_container)
        social_layout.setSpacing(13)  # Отступ в 13px между иконками
        social_layout.setAlignment(Qt.AlignBottom)  # Выровнять влево и вниз

        # Discord (кликабельное)
        ds_image_path = resource_path("assets/ds.png")
        self.ds_image = QLabel()
        self.ds_image.setPixmap(QPixmap(ds_image_path).scaled(44, 44, Qt.KeepAspectRatio))
        self.ds_image.setCursor(Qt.PointingHandCursor)
        self.ds_image.mouseReleaseEvent = self.ds_link
        social_layout.addWidget(self.ds_image)

        # Telegram (кликабельное)
        tg_image_path = resource_path("assets/tg.png")
        self.tg_image = QLabel()
        self.tg_image.setPixmap(QPixmap(tg_image_path).scaled(44, 44, Qt.KeepAspectRatio))
        self.tg_image.setCursor(Qt.PointingHandCursor)
        self.tg_image.mouseReleaseEvent = self.tg_link
        social_layout.addWidget(self.tg_image)

        # VK (кликабельное)
        vk_image_path = resource_path("assets/vk.png")
        self.vk_image = QLabel()
        self.vk_image.setPixmap(QPixmap(vk_image_path).scaled(44, 44, Qt.KeepAspectRatio))
        self.vk_image.setCursor(Qt.PointingHandCursor)
        self.vk_image.mouseReleaseEvent = self.vk_link
        social_layout.addWidget(self.vk_image)

        # Добавляем контейнер в навигационную панель
        nav_layout.addWidget(social_container)

        # Правая панель (Основное содержимое)
        self.main_content = QWidget()
        self.main_content.setStyleSheet("background: transparent;")  
        self.main_layout = QVBoxLayout(self.main_content)  

        main_layout.addWidget(self.nav_panel)
        main_layout.addWidget(self.main_content, 1)

        # Устанавливаем начальную активную вкладку
        self.set_active_button(self.buttons[0], "Программы")

    def site_link(self, event):
        QDesktopServices.openUrl(QUrl("https://purecs2.ru/")) 

    def ds_link(self, event):
        QDesktopServices.openUrl(QUrl("https://discord.gg/purecs2/")) 

    def tg_link(self, event):
        QDesktopServices.openUrl(QUrl("https://t.me/purecs2/")) 

    def vk_link(self, event):
        QDesktopServices.openUrl(QUrl("https://vk.com/purecs2/")) 

    def set_active_button(self, button, page_name):
        if self.active_button:
            self.active_button.setStyleSheet("""
                color: white;
                background-color: #2c6db1;
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
            """)
        button.setStyleSheet("""
            color: white;
            background-color: #225081;
            border: none;
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
        """)
        self.active_button = button

        # Показать контент выбранной страницы
        self.show_page(page_name)

    def show_page(self, page_name):
        # Очистить текущий контент
        for i in range(self.main_content.layout().count()):
            item = self.main_content.layout().itemAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Создать новый контент для выбранной страницы
        if page_name == "Программы":
            page_content = ProgramsPage()
        elif page_name == "Steam":
            page_content = SteamPage()
        elif page_name == "Другое":
            page_content = OtherPage()
        #elif page_name == "USB":
        #    page_content = USBPage()

        self.main_layout.addWidget(page_content)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
