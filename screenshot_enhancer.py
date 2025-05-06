from tkinter import *
from tkinter import messagebox

class EnhanceSliderWindow(Toplevel):
    def __init__(self, root, name, enhance, image, update_method):
        self.name = name
        self.enhancer = enhance(image)
        self.root = super().__init__(root)
        self.original = image
        self.image = image.copy()
        self.update_method = update_method
        self.protocol("WM_DELETE_WINDOW", self.window_exit)

        self.init()

        self.factor = DoubleVar(value=1.0)
        self.scroll = Scale(self, label=self.name, from_=0.0, to=2.0, resolution=0.1, variable=self.factor, orient='horizontal', command=self.value_changed)

        self.apply_button = Button(self, text="Применить", command=self.close)
        self.cancel_button = Button(self, text="Отмена", command=self.cancel)

        self.draw_widgets()

    # Метод инициализации
    def init(self):
        self.title(f"SSM Enchance")
        self.iconbitmap(r"Diplom/icons/SSM Enhancer.ico")
        self.grab_focus()

    # Метод привлечение фокуса пользователя
    def grab_focus(self):
        self.grab_set()
        self.focus_force()        

    # Метод отрисовки виджетов
    def draw_widgets(self):
        self.scroll.pack(fill="x", expand=1, padx=5, pady=5)
        self.apply.pack(side="left", expand=1, padx=5, pady=5)
        self.cancel.pack(side="left", expand=1, padx=5, pady=5)

    # Метод обновления значения усиления
    def value_changed(self, value):
        self.image = self.enhancer.enhance(self.factor.get())
        self.update_method(self.image)
    
    # Метод отмены, возвращающего первоначального скриншота
    def cancel(self):
        self.update_method(self.original)
        self.close()

    # Метод подтверждения выхода из программы
    def window_exit(self):
        close = messagebox.askyesno("Выйти?", "Вы уверена что вы хотите выйти?")
        if close:
            self.close()

    # Метод очистки памяти
    def data_clear(self):
        self.original = None
        self.enhancer = None
        self.image = None  

    # Метод закрытия программы
    def close(self):
        self.data_clear()        
        self.destroy()
    

    