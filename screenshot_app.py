from tkinter import *
from screenshot_editor import EditorWindow
from PIL import Image as PLImage
from PIL import ImageTk
import pyautogui as pag
from time import sleep

version = "1.0"

class ScreenshotWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("200x100")
        self.root.resizable(False, False)
        self.root.title("SSM")
        self.root.iconbitmap(r"Diplom/icons/SSM.ico")

        img = PLImage.open(r"Diplom/icons/Screenshot_icon.png")
        img = img.resize((20, 20))
        self.screenshot_icon = ImageTk.PhotoImage(img)
        self.current_screenshot = None
    
    # Метод отрисовки виджетов на экране
    def show_widgets(self):
        Button(self.root, text="Создать", image=self.screenshot_icon, compound=LEFT, justify=CENTER, width=145, height=25, borderwidth=5, command=self.screenshot).pack()
        Label(self.root, text="Нажмите на кнопку создать, чтобы создать скриншот.", width=145, height=25, wraplength=150).pack()

    # Метод запускающий отрисовку виджетов и запуск цикла программы
    def run(self):
        self.show_widgets()
        self.root.mainloop()    

    # Метод создания скриншота
    def screenshot(self):
        self.root.withdraw()
        sleep(0.3)
        self.current_screenshot = pag.screenshot()
        self.create_editor(screenshot=self.current_screenshot)
        self.root.deiconify()

    # Метод запускающий редактор для скриншота
    def create_editor(self, screenshot):
        EditorWindow(self.root, screenshot)
        self.current_screenshot = None

if __name__ == "__main__":
    if version == "1.0":
        program = ScreenshotWindow()
        program.run()