# 🎯 purecs2 CheckerCheat

**purecs2 CheckerCheat** — инструмент для сканирования и выявления следов читов в системе.

## ⚡ Функционал
✔️ **Пакет нужных программ** — все нужные программы для поиска читов.
✔️ **Steam-файлы** — просмотр `loginusers.vdf` для анализа.
✔️ **Интеграция с Discord** — (если он запущен) отображаем статус.

## 🛠️ Установка и запуск
```bash
git clone https://github.com/immanuel1618/purecs2-Checker-Cheat.git
cd purecs2_checkercheat
pip install -r requirements.txt
python main.py
```

## 📦 Компиляция в EXE
Собрать `.exe` можно с помощью **PyInstaller** и **PyArmor**:
```bash
pyarmor obfuscate --recursive main.py
pyinstaller --icon=logo.ico --onefile --windowed --noupx \
    --add-data "app;app" --add-data "assets;assets" dist/main/main.py
```

## ❓ FAQ
🔹 **Программа не запускается?**  
➜ Проверь, установлены ли зависимости: `pip install -r requirements.txt`.

🔹 **Не отображается Discord Rich Presence?**  
➜ Убедись, что **Discord запущен** перед запуском программы.

🔹 **Steam не найден?**  
➜ Файл `loginusers.vdf` может быть на другом диске, попробуй поискать.

## 👨‍💻 Контакты
📌 Site: [бибабуп](https://immanuel.nna1618.com/)  
📌 Telegram: [@StreetPN](https://t.me/StreetPN)  
📌 GitHub: [immanuel1618](https://github.com/immanuel1618)

---
💙 Сделано с душой. Если проект полезен — жми ⭐ в репо!

