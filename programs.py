import os
import subprocess
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, QFormLayout
from PySide6.QtCore import Qt

class ProgramsPage(QWidget):
    def __init__(self):
        super().__init__()

        # Основной макет
        main_layout = QHBoxLayout(self)

        # Левая панель - Анализ файлов / Директорий ПК
        left_panel = QVBoxLayout()
        left_group = QGroupBox("Анализ файлов / Директорий ПК")
        left_group.setStyleSheet("background-color: rgba(33, 76, 122, 40); color: white; border-radius: 10px; padding: 10px;")
        left_layout = QVBoxLayout(left_group)
        left_group.setAlignment(Qt.AlignCenter) 
        left_group.setStyleSheet("""
            background-color: rgba(33, 76, 122, 40);
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            text-align: center;
        """)



        buttons = [
            ("Everything", "Everything.exe"),
            ("Shellbag Analyzer", "ShellbagAnalyzer.exe"),
            ("OpenedFilesView", "OpenedFilesView.exe"),
            ("UserAssistView", "UserAssistView.exe"),
            ("ExecutedProgramsList", "ExecutedProgramsList.exe"),
            ("LastActivityView", "LastActivityView.exe"),
        ]

        for label, exe_file in buttons:
            btn = QPushButton(label)
            btn.setStyleSheet(self.button_style())
            btn.clicked.connect(lambda checked, exe=exe_file: self.run_application(exe))
            left_layout.addWidget(btn)

        left_panel.addWidget(left_group)

        # Правая панель
        right_panel = QVBoxLayout()
        
        # Анализ браузеров / Веб-приложений
        browser_group = QGroupBox("Анализ браузеров / Веб-приложений")
        browser_group.setStyleSheet("background-color: rgba(33, 76, 122, 40); color: white; border-radius: 10px; padding: 10px;")
        browser_layout = QVBoxLayout(browser_group)
        browser_group.setAlignment(Qt.AlignCenter) 
        browser_group.setStyleSheet("""
            background-color: rgba(33, 76, 122, 40);
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            text-align: center;
        """)

        browser_buttons = [
            ("BrowsingHistoryView", "BrowsingHistoryView.exe"),
            ("Browser Downloads View", "BrowserDownloadsView.exe")
        ]

        for label, exe_file in browser_buttons:
            btn = QPushButton(label)
            btn.setStyleSheet(self.button_style())
            btn.clicked.connect(lambda checked, exe=exe_file: self.run_application(exe))
            browser_layout.addWidget(btn)

        right_panel.addWidget(browser_group)

        # Анализ процесса игры
        game_process_group = QGroupBox("Анализ процесса игры")
        game_process_group.setStyleSheet("background-color: rgba(33, 76, 122, 40); color: white; border-radius: 10px; padding: 10px;")
        game_process_layout = QVBoxLayout(game_process_group)
        game_process_group.setAlignment(Qt.AlignCenter)
        game_process_group.setStyleSheet("""
            background-color: rgba(33, 76, 122, 40);
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            text-align: center;
        """)

        game_process_buttons = [
            ("System Informer", "SystemInformer/SystemInformer.exe"),
        ]

        for label, exe_file in game_process_buttons:
            btn = QPushButton(label)
            btn.setStyleSheet(self.button_style())
            btn.clicked.connect(lambda checked, exe=exe_file: self.run_application(exe))
            game_process_layout.addWidget(btn)

        right_panel.addWidget(game_process_group)

        # Анализ реестра и Trace
        registry_group = QGroupBox("Реестр и Trace")
        registry_group.setStyleSheet("background-color: rgba(33, 76, 122, 40); color: white; border-radius: 10px; padding: 10px;")
        registry_layout = QVBoxLayout(registry_group)
        registry_group.setAlignment(Qt.AlignCenter) 
        registry_group.setStyleSheet("""
            background-color: rgba(33, 76, 122, 40);
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            text-align: center;
        """)

        registry_buttons = [
            ("Registry Finder", "RegistryFinder.exe"),
            ("JournalTrace", "JournalTrace.exe"),
        ]

        for label, exe_file in registry_buttons:
            btn = QPushButton(label)
            btn.setStyleSheet(self.button_style())
            btn.clicked.connect(lambda checked, exe=exe_file: self.run_application(exe))
            registry_layout.addWidget(btn)

        right_panel.addWidget(registry_group)

        # Добавление панелей в основной макет
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

    def button_style(self):
        return """
            color: white;
            background-color: #225081;
            border: none;
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            transition: all 0.3s;
        """




    def run_application(self, exe_file):
        if getattr(sys, 'frozen', False):
            app_path = os.path.join(sys._MEIPASS, "app", exe_file)
        else:
            app_path = os.path.join(os.path.dirname(__file__), "app", exe_file)

        if os.path.exists(app_path):
            subprocess.Popen([app_path])  
            
            if exe_file == "Everything.exe":
                txt_file = os.path.join(os.path.dirname(app_path), "./txt/everything.txt")
                if os.path.exists(txt_file):
                    subprocess.Popen(["notepad.exe", txt_file])  
                else:
                    print(f"Файл everything.txt не найден рядом с {exe_file}.")
            
            
            if exe_file == "LastActivityView.exe":
                txt_file = os.path.join(os.path.dirname(app_path), "./txt/LASTACTIVITY.txt")
                if os.path.exists(txt_file):
                    subprocess.Popen(["notepad.exe", txt_file])  
                else:
                    print(f"Файл LASTACTIVITY.txt не найден рядом с {exe_file}.")

            
            if exe_file == "RegistryFinder.exe":
                txt_file = os.path.join(os.path.dirname(app_path), "./txt/regdit.txt")
                if os.path.exists(txt_file):
                    subprocess.Popen(["notepad.exe", txt_file])  
                else:
                    print(f"Файл regdit.txt не найден рядом с {exe_file}.")

        else:
            print(f"Приложение {exe_file} не найдено в папке app.")
