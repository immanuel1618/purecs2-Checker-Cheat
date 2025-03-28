import os
import subprocess
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PySide6.QtCore import Qt


class NoProgramsPage(QWidget):
    def __init__(self):
        super().__init__()

        # Основной макет
        main_layout = QHBoxLayout(self)

        # Левая панель (3 кнопки)
        left_panel = QVBoxLayout()
        left_group = QGroupBox("Система")
        left_group.setStyleSheet(self.group_style())
        left_layout = QVBoxLayout(left_group)
        left_group.setAlignment(Qt.AlignCenter) 

        buttons_left = [
            ("Открыть реестр", lambda: (self.run_command("start regedit"), self.run_application(r"app\txt\regdit.txt"))),
            ("Открыть recent/prefetch/temp", lambda: self.run_application(r"app\bat\recentprefetchtemp.bat")),
            ("Открыть сайты", lambda: self.run_application(r"app\bat\site.bat")),
            ("Открыть Мой компьютер", lambda: self.run_command("explorer shell:MyComputerFolder")),
        ]

        for label, action in buttons_left:
            btn = self.create_button(label, action)
            left_layout.addWidget(btn)

        left_panel.addWidget(left_group)

        # Правая панель (3 кнопки)
        right_panel = QVBoxLayout()
        right_group = QGroupBox("Дополнительно")
        right_group.setStyleSheet(self.group_style())
        right_layout = QVBoxLayout(right_group)
        right_group.setAlignment(Qt.AlignCenter) 

        buttons_right = [
            ("Панель управления NVIDIA", lambda: self.run_command("start nvcplui")),
            ("Использование данных", lambda: self.run_command("start ms-settings:datausage")),
            ("Экранная клавиатура", lambda: self.run_command("osk")),
            ("Службы Windows", lambda: self.run_command("services.msc")),
        ]

        for label, action in buttons_right:
            btn = self.create_button(label, action)
            right_layout.addWidget(btn)

        right_panel.addWidget(right_group)

        # Добавляем в основной макет
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 1)

    def run_command(self, command):
        """Запускает команду в shell"""
        subprocess.Popen(command, shell=True)

    def run_application(self, path):
        """Открывает файл или программу, проверяя несколько возможных путей."""
        possible_paths = [
            path,  # Относительный путь
            os.path.join(os.path.dirname(__file__), path),  # Относительно скрипта
            os.path.join(os.getcwd(), path)  # Относительно текущей директории
        ]

        for app_path in possible_paths:
            if os.path.exists(app_path):
                subprocess.Popen([app_path], shell=True)  # Запускаем файл
                return

        print(f"Файл {path} не найден.")


    def create_button(self, text, action):
        """Создаёт стилизованную кнопку"""
        btn = QPushButton(text)
        btn.setStyleSheet(self.button_style())
        btn.clicked.connect(action)
        return btn

    def group_style(self):
        """CSS-стиль для QGroupBox"""
        return """
            background-color: rgba(33, 76, 122, 40);
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        """

    def button_style(self):
        """CSS-стиль для кнопок"""
        return """
            color: white;
            background-color: #225081;
            border: none;
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
        """

