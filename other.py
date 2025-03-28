import psutil
import platform
import subprocess
import wmi
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGroupBox, QFormLayout, QPushButton
from PySide6.QtCore import Qt, QThread, Signal
from screeninfo import get_monitors


class SystemInfoThread(QThread):
    update_signal = Signal(str, str)

    def run(self):
        self.update_signal.emit("Количество экранов:", str(self.get_screen_count()))
        self.update_signal.emit("Система:", platform.system())
        self.update_signal.emit("Объем ОЗУ:", self.get_ram_size())
        self.update_signal.emit("Процессор:", self.get_cpu_info())
        self.update_signal.emit("Видеокарта:", self.get_gpu_info())
        self.update_signal.emit("Материнская плата:", self.get_motherboard_info())

    def get_screen_count(self):
        try:
            monitors = get_monitors()
            return len(monitors)
        except Exception:
            return "Неизвестно"

    def get_ram_size(self):
        ram_size = psutil.virtual_memory().total / (1024 ** 3)  # в гигабайтах
        return f"{ram_size:.2f} GB"

    def get_cpu_info(self):
        try:
            c = wmi.WMI()
            cpu_info = c.query("SELECT Name FROM Win32_Processor")
            return cpu_info[0].Name if cpu_info else "Неизвестно"
        except Exception:
            return "Неизвестно"

    def get_gpu_info(self):
        try:
            gpu_info = subprocess.check_output('wmic path win32_videocontroller get caption', shell=True)
            return gpu_info.decode().strip().split("\n")[1].strip()
        except Exception:
            return "Неизвестно"

    def get_motherboard_info(self):
        try:
            c = wmi.WMI()
            motherboard_info = c.query("SELECT Manufacturer, Product FROM Win32_BaseBoard")
            return f"{motherboard_info[0].Manufacturer} - {motherboard_info[0].Product}" if motherboard_info else "Неизвестно"
        except Exception:
            return "Неизвестно"


class OtherPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Information")
        self.setStyleSheet("""
            background-color: #2e2e2e;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 14px;
        """)

        # Главный макет
        main_layout = QHBoxLayout(self)

        # Левое окно
        left_layout = QVBoxLayout()
        self.system_info_group = QGroupBox("Системная информация")
        self.system_info_group.setStyleSheet("""
            background-color: rgba(33, 76, 122, 40); 
            color: white;
            border-radius: 10px;
            padding: 10px;
        """)
        left_layout.addWidget(self.system_info_group)

        system_info_layout = QFormLayout()
        self.screen_count_label = QLabel("Определение...")
        self.system_label = QLabel("Определение...")
        self.ram_size_label = QLabel("Определение...")
        self.cpu_label = QLabel("Определение...")
        self.gpu_label = QLabel("Определение...")
        self.motherboard_label = QLabel("Определение...")

        system_info_layout.addRow("Количество экранов:", self.screen_count_label)
        system_info_layout.addRow("Система:", self.system_label)
        system_info_layout.addRow("Объем ОЗУ:", self.ram_size_label)
        system_info_layout.addRow("Процессор:", self.cpu_label)
        system_info_layout.addRow("Видеокарта:", self.gpu_label)
        system_info_layout.addRow("Материнская плата:", self.motherboard_label)

        self.system_info_group.setLayout(system_info_layout)

        # Добавление правого окна в основное
        main_layout.addLayout(left_layout)


        # Получения данных о системе
        self.system_info_thread = SystemInfoThread()
        self.system_info_thread.update_signal.connect(self.update_system_info)
        self.system_info_thread.start()

    def update_system_info(self, label, value):
        if label == "Количество экранов:":
            self.screen_count_label.setText(value)
        elif label == "Система:":
            self.system_label.setText(value)
        elif label == "Объем ОЗУ:":
            self.ram_size_label.setText(value)
        elif label == "Процессор:":
            self.cpu_label.setText(value)
        elif label == "Видеокарта:":
            self.gpu_label.setText(value)
        elif label == "Материнская плата:":
            self.motherboard_label.setText(value)
