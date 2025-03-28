import os
import vdf
import requests
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from datetime import datetime, timedelta
import sys
from searchsteam import get_loginusers_vdf_path

STEAM_API_KEY = "5A52CDFE888E5EC78232A572FA8D99F4"  # Вставь свой API-ключ

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        app_data_path = os.path.join(os.getenv('APPDATA'), 'MyApp') 
        os.makedirs(app_data_path, exist_ok=True)
        base_path = app_data_path
    return os.path.join(base_path, relative_path)

def get_steam_account_info(steamid):
    """Получает информацию о VAC и игровых блокировках через Steam API."""
    api_url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={STEAM_API_KEY}&steamids={steamid}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if "players" in data and data["players"]:
            player = data["players"][0]
            if player["NumberOfGameBans"] == 0 and player["NumberOfVACBans"] == 0:
                vac_status = "VAC 🟢"
            else:
                vac_status = f"VAC 🔴 game = {player['NumberOfGameBans'] + player['NumberOfVACBans']}, days = {player['DaysSinceLastBan']}"
        else:
            vac_status = "Неизвестно"
        return vac_status
    except Exception as e:
        print(f"Ошибка запроса API Steam: {e}")
        return "VAC ❓"

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
        main_layout = QVBoxLayout(self)
        self.account_list = QListWidget()
        main_layout.addWidget(self.account_list)
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
        if not os.path.exists(vdf_file_path):
            print(f"Файл не найден: {vdf_file_path}")
            return []
        try:
            with open(vdf_file_path, 'r', encoding='utf-8') as file:
                vdf_data = vdf.load(file)
        except Exception as e:
            print(f"Ошибка при чтении VDF файла: {e}")
            return []
        accounts = []
        users = vdf_data.get('users', {})
        for steamid, account_data in users.items():
            accounts.append({
                'steamid': steamid,
                'AccountName': account_data.get('AccountName'),
                'PersonaName': account_data.get('PersonaName'),
                'Timestamp': account_data.get('Timestamp')
            })
        return accounts

    def get_avatar(self, steamid):
        avatar_cache_path = os.path.expandvars(r'C:\\Program Files (x86)\\Steam\\config\\avatarcache')
        avatar_file = os.path.join(avatar_cache_path, f'{steamid}.jpg')
        if not os.path.exists(avatar_file):
            avatar_file = os.path.join(avatar_cache_path, f'{steamid}.png')
        if not os.path.exists(avatar_file):
            avatar_file = resource_path('assets/noava.png')
        return avatar_file

    def display_account(self, account_info):
        list_item = QListWidgetItem()
        account_widget = QWidget()
        account_layout = QHBoxLayout()
        avatar_file = self.get_avatar(account_info['steamid'])
        avatar = QLabel()
        pixmap = QPixmap(avatar_file)
        if pixmap.isNull():
            pixmap = QPixmap(resource_path('assets/noava.png'))
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        avatar.setPixmap(pixmap)
        avatar.setFixedSize(50, 50)
        account_layout.addWidget(avatar)
        
        def convert_timestamp_to_msk(timestamp):
            timestamp = int(timestamp) if isinstance(timestamp, str) else timestamp
            utc_time = datetime.utcfromtimestamp(timestamp)
            msk_time = utc_time + timedelta(hours=3)
            return msk_time.strftime("%Y-%m-%d %H:%M:%S")
        
        vac_status = get_steam_account_info(account_info['steamid'])
        account_details = QLabel(f"ID: {account_info['steamid']}\n"
                                 f"AccountName: {account_info['AccountName']}\n"
                                 f"PersonaName: {account_info['PersonaName']}\n"
                                 f"Last Login (MSK): {convert_timestamp_to_msk(account_info['Timestamp'])}\n"
                                 f"{vac_status}")
        account_details.setTextInteractionFlags(Qt.TextSelectableByMouse)
        account_layout.addWidget(account_details)
        account_widget.setLayout(account_layout)
        list_item.setSizeHint(account_widget.sizeHint())
        self.account_list.addItem(list_item)
        self.account_list.setItemWidget(list_item, account_widget)
