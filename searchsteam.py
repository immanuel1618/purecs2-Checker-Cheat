import os
import vdf
import winreg

def get_all_drives():
    """Получает список доступных дисков в системе (C:, D:, E:, ...)."""
    from string import ascii_uppercase
    available_drives = [f"{d}:\\" for d in ascii_uppercase if os.path.exists(f"{d}:\\")]
    return available_drives

def search_steam_on_drives():
    """Ищет папку Steam на всех дисках (C:, D:, E:, ...)."""
    for drive in get_all_drives():
        steam_path = os.path.join(drive, "Steam")
        if os.path.exists(os.path.join(steam_path, "config", "loginusers.vdf")):
            return steam_path
    return None

def get_steam_path():
    """Определяет путь к установке Steam, проверяя стандартные пути, реестр и все диски."""
    possible_paths = [
        r'C:\Program Files (x86)\Steam',
        r'C:\Program Files\Steam',
        os.path.expandvars(r'%PROGRAMFILES(X86)%\Steam'),
        os.path.expandvars(r'%PROGRAMFILES%\Steam'),
        os.path.expandvars(r'%LOCALAPPDATA%\Steam'),
        os.path.expandvars(r'%APPDATA%\Steam')
    ]

    # Проверяем стандартные пути
    for path in possible_paths:
        config_path = os.path.join(path, 'config', 'loginusers.vdf')
        if os.path.exists(config_path):
            return path

    # Пробуем найти путь в реестре
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            steam_path = os.path.normpath(steam_path)  # Приводим путь к стандартному виду
            if os.path.exists(os.path.join(steam_path, 'config', 'loginusers.vdf')):
                return steam_path
    except FileNotFoundError:
        pass

    # Если в стандартных местах и в реестре не нашли — ищем на всех дисках
    return search_steam_on_drives()

def get_loginusers_vdf_path():
    """Возвращает путь к loginusers.vdf или None, если файл не найден."""
    steam_path = get_steam_path()
    if steam_path:
        return os.path.join(steam_path, 'config', 'loginusers.vdf')
    return None

# надоело писать комменты ппц
vdf_path = get_loginusers_vdf_path()
if vdf_path:
    print(f"Файл loginusers.vdf найден: {vdf_path}")
else:
    print("Не удалось найти файл loginusers.vdf")
