import os
import vdf
import hashlib
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from datetime import datetime, timezone, timedelta
import sys
from searchsteam import get_loginusers_vdf_path

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        app_data_path = os.path.join(os.getenv('APPDATA'), 'MyApp') 
        if not os.path.exists(app_data_path):
            os.makedirs(app_data_path)
        base_path = app_data_path

    return os.path.join(base_path, relative_path)


class SteamPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Steam Accounts")
        self.setStyleSheet("""
            background-color: rgba(33, 76, 122, 40);
            color: white;
            font-family: Arial, sans-serif;
            font-size: 14px;
        """)

        # Главный макет
        main_layout = QVBoxLayout(self)

        # Список аккаунтов
        self.account_list = QListWidget()
        main_layout.addWidget(self.account_list)

        # Загружаем данные из loginusers.vdf
        self.load_steam_accounts()

    def load_steam_accounts(self):
        steam_accounts = self.read_vdf_file()

        if steam_accounts:
            for account in steam_accounts:
                self.display_account(account)
        else:
            print("Не удалось найти или загрузить аккаунты из файла.")

    def read_vdf_file(self):
        vdf_file_path = get_loginusers_vdf_path()

        
        print(f"Пытаемся открыть файл: {vdf_file_path}")
        if not os.path.exists(vdf_file_path):
            print(f"Файл не найден: {vdf_file_path}")
            return []

        try:
            with open(vdf_file_path, 'r', encoding='utf-8') as file:
                vdf_data = vdf.load(file)
            print("Файл успешно загружен и прочитан.")
        except Exception as e:
            print(f"Ошибка при чтении VDF файла: {e}")
            return []

        accounts = []
        users = vdf_data.get('users', {})
        print(f"Найдено аккаунтов: {len(users)}")

        for steamid, account_data in users.items():
            accounts.append({
                'steamid': steamid,
                'AccountName': account_data.get('AccountName'),
                'PersonaName': account_data.get('PersonaName'),
                'Timestamp': account_data.get('Timestamp')
            })

        return accounts

    def get_avatar(self, steamid):
        avatar_cache_path = os.path.expandvars(r'C:\Program Files (x86)\Steam\config\avatarcache')
        avatar_file = os.path.join(avatar_cache_path, f'{steamid}.jpg')

        if not os.path.exists(avatar_file):
            avatar_file = os.path.join(avatar_cache_path, f'{steamid}.png')

        # Если аватарка не найдена, используем "noava.png"
        if not os.path.exists(avatar_file):
            avatar_file = resource_path('assets/noava.png')

        return avatar_file

    def display_account(self, account_info):
        list_item = QListWidgetItem()

        account_widget = QWidget()
        account_layout = QHBoxLayout()

        # Получаем аватарку
        avatar_file = self.get_avatar(account_info['steamid'])
        avatar = QLabel()
        if avatar_file:
            pixmap = QPixmap(avatar_file)
            pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            avatar.setPixmap(pixmap)
        if pixmap.isNull():
            pixmap = QPixmap(resource_path('assets/noava.png'))
            pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            avatar.setPixmap(pixmap)
        
        avatar.setFixedSize(50, 50)
        account_layout.addWidget(avatar)

        def convert_timestamp_to_msk(timestamp):
            # Преобразует Unix Timestamp в дату в формате MSK.
            timestamp = int(timestamp) if isinstance(timestamp, str) else timestamp
            utc_time = datetime.utcfromtimestamp(timestamp)  # Время в UTC
            msk_time = utc_time + timedelta(hours=3)  # Добавляем 3 часа для MSK
            return msk_time.strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату

        # Добавление текста
        account_details = QLabel(f"ID: {account_info['steamid']}\n"
                                f"AccountName: {account_info['AccountName']}\n"
                                f"PersonaName: {account_info['PersonaName']}\n"
                                f"Last Login (MSK): {convert_timestamp_to_msk(account_info['Timestamp'])}")
        account_layout.addWidget(account_details)

        account_widget.setLayout(account_layout)
        list_item.setSizeHint(account_widget.sizeHint())
        self.account_list.addItem(list_item)
        self.account_list.setItemWidget(list_item, account_widget)
