from tkinter import *
from tkinter import messagebox
import os


from assets.log_creator import add_new_log

class EnhanceSliderWindow(Toplevel):
    def __init__(self, root, name, enhance, image, update_method):
        self.name = name
        self.enhancer = enhance(image)
        self.root = super().__init__(root)
        self.geometry(f"{200}x{100}+{(self.winfo_screenwidth() // 2) - (200 // 2)}+{(self.winfo_screenheight() // 2) - (100 // 2)}")
        self.resizable(False, False)
        self.original = image
        self.image = image.copy()
        self.update_method = update_method
        self.protocol("WM_DELETE_WINDOW", self.window_exit)


        self.init()

        self.factor = DoubleVar(value=1.0)
        self.scroll = Scale(self, label=self.name, from_=0.0, to=2.0, resolution=0.1,
                            variable=self.factor, orient='horizontal', command=self.value_changed)

        self.apply_button = Button(self, text="Применить", command=self.close)
        self.cancel_button = Button(self, text="Отмена", command=self.cancel)

        self.draw_widgets()

    # Метод инициализации
    def init(self):
        self.title(f"SSM Enchance")
        self.iconbitmap(f"{os.path.dirname(os.path.abspath(__file__))}\\SSM Enhancer.ico")
        self.grab_focus()

    # Метод привлечение фокуса пользователя
    def grab_focus(self):
        self.grab_set()
        self.focus_force()        

    # Метод отрисовки виджетов
    def draw_widgets(self):
        add_new_log(f"[INFO] - EnhanceSliderWindow: Отрисовка виджетов класса EnhanceSliderWindow\n")
        self.scroll.pack(fill="x", expand=1, padx=5, pady=5)
        self.apply_button.pack(side="left", expand=1, padx=5, pady=5)
        self.cancel_button.pack(side="left", expand=1, padx=5, pady=5)

    # Метод обновления значения усиления
    def value_changed(self, value):
        add_new_log(f"[INFO] - EnhanceSliderWindow: Изменение значения - {value}\n")
        self.image = self.enhancer.enhance(self.factor.get())
        self.update_method(self.image)
    
    # Метод отмены, возвращающего первоначального скриншота
    def cancel(self):
        add_new_log(f"[INFO] - EnhanceSliderWindow: Отмена настройки\n")
        self.update_method(self.original)
        self.close()

    # Метод подтверждения выхода из программы
    def window_exit(self):
        close = messagebox.askyesno("Выйти?", "Вы уверена что вы хотите выйти?")
        if close:
            self.close()

    # Метод закрытия программы
    def close(self):
        add_new_log(f"[INFO] - EnhanceSliderWindow: Закрытие настройки\n")
        self.original = None
        self.enhancer = None
        self.image = None         
        self.destroy()
    

    