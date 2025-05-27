from tkinter import *
from tkinter import messagebox
from time import sleep
from PIL import Image, ImageTk
import pyautogui as pag
import webbrowser
import os


from assets.version_check import check_for_updates, get_version
from assets.log_creator import log_cleaner, add_new_log
from assets.screenshot_editor import EditorWindow

class ScreenshotWindow:
    def __init__(self):
        dir = os.path.dirname(os.path.abspath(__file__))      
        
        self.root = Tk()
        self.root.geometry(f"{200}x{100}+{(self.root.winfo_screenwidth() // 2) - (200 // 2)}+{(self.root.winfo_screenheight() // 2) - (100 // 2)}")
        self.root.resizable(False, False)
        self.root.title("SSM")
        self.root.iconbitmap(f"{dir}\\assets\\SSM.ico")
        self.exe_count = 0

        img = Image.open(f"{dir}\\assets\\Screenshot_icon.png")
        img = img.resize((20, 20))
        self.screenshot_icon = ImageTk.PhotoImage(img)
        self.current_screenshot = None
    
    # Метод отрисовки виджетов на экране
    def show_widgets(self):
        add_new_log("[INFO] - ScreenshotWindow: Отрисовка виджетов скриншотера\n")
        Button(self.root, text="Создать",
                image=self.screenshot_icon,
                compound=LEFT, justify=CENTER,
                width=145, height=25, borderwidth=5,
                command=self.screenshot).pack()
        Label(self.root, text="Нажмите на кнопку создать, чтобы создать скриншот.",
              width=145, height=25, wraplength=150).pack()

    # Метод запускающий отрисовку виджетов и запуск цикла программы
    def run(self):      
        self.show_widgets()
        self.grab_focus() 
        self.root.mainloop() 

    def grab_focus(self):
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-topmost", False)

    # Метод создания скриншота
    def screenshot(self):
        self.root.withdraw()
        sleep(0.3)
        self.current_screenshot = pag.screenshot()
        add_new_log(f"[INFO] - ScreenshotWindow: Создание скриншота {self.current_screenshot}\n")
        self.create_editor(screenshot=self.current_screenshot)
        self.root.deiconify()

    # Метод запускающий редактор для скриншота
    def create_editor(self, screenshot):
        add_new_log("[INFO] - ScreenshotWindow: Запуск класса редактора EditorWindow\n")
        EditorWindow(self.root, screenshot)
        self.current_screenshot = None

if __name__ == "__main__": # Проверка что это исполняемый скрипт
    log_cleaner()
    version = check_for_updates() # Записывает в переменную версию загруженную на облако
    if check_for_updates()[0] == False: # Если версия актуальная запускает приложение
        program = ScreenshotWindow()
        program.run()
    else:
        # Спрашивает пользователя хочет ли он обновить приложение
        check = messagebox.askyesno("Доступна новая версия!",
                                    f"Доступна новая версия. Желаете ли перейти c версии {get_version()} до версии {version[1]}?")
        if check: # Если ответ да, то перенаправляет пользователя на GitHub в раздел релизов
            webbrowser.open("https://github.com/nepk2/screenshot_app/releases")
        else:
            # Иначе запускает программу
            program = ScreenshotWindow()
            program.run()

add_new_log("[INFO] - ScreenshotWindow: Закрытие программы\n")
add_new_log("[INFO] - Start: LOG END\n")