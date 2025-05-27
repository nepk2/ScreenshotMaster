import datetime
import os

# Поиск директории логов
dir = os.path.dirname(os.path.abspath(__file__))

# Запись директории в переменную 
file_dir = f"{dir}\\log.txt" 

# Функция начала записи логов
def log_cleaner(): 
    with open(file_dir, "w") as log_file:
        log_file.write(f"({datetime.datetime.now().strftime("%H:%M:%S")}) [INFO] - Start: LOG START\n")

# Функция записи логов
def add_new_log(log_string):
    with open(file_dir, "a") as log_file:
        log_file.write(f'({datetime.datetime.now().strftime("%H:%M:%S")}) {log_string}')
