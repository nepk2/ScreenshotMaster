import requests
import json
import os

from assets.log_creator import add_new_log


def check_for_updates():
    # URL к raw-файлу с версией на GitHub
    version_url = "https://raw.githubusercontent.com/nepk2/ScreenshotMaster/refs/heads/main/assets/version.json"
    
    try:
        add_new_log(f"[INFO] - version_checker: Проверка актуальности программы...\n")
        response = requests.get(version_url)
        response.raise_for_status()  # Проверяем на ошибки HTTP
        
        remote_data = response.json()
        remote_version = remote_data.get("version")
        
        if remote_version != get_version():
            add_new_log(f"[INFO] - version_checker: Найдено новое обновление\n")        
            return True, remote_version  # Доступно обновление
        add_new_log(f"[INFO] - version_checker: Новой версии не найдено\n")   
        return False, get_version()  # Версия актуальна
    
    except requests.RequestException as e:
        add_new_log(f"[ERROR] - version_checker: Ошибка при проверке обновлений: {e}\n") 
        print(f"Ошибка при проверке обновлений: {e}")
        return False, get_version()

def get_version():
    add_new_log(f"[INFO] - version_checker: Проверка версии установленной программы\n") 
    with open(f"{os.path.dirname(os.path.abspath(__file__))}\\version.json", "r") as file:
        data = json.load(file)    
    return data["version"]