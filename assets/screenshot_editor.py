from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
import pyautogui as pag
import numpy as np
import os


from assets.сlipboard_buffer import copy_image_to_clipboard
from assets.log_creator import add_new_log
from assets.screenshot_enhancer import EnhanceSliderWindow

class EditorWindow:
    def __init__(self, parent, screenshot):
        self.dir = os.path.dirname(os.path.abspath(__file__))  

        self.root = Toplevel(parent) # Создание дочернего окна от основной программы
        self.root.title("SSM Editor")
        self.root.iconbitmap(f"{self.dir}\\SSM Editor.ico")        
        self.photo = screenshot # Запись скриншота в переменную
        self.fPhoto = self.photo # Фальшивка для демонстрации (нс)
        self.curSize = 100 # Текущее масштабирование (нс)
        self.history_buffer = []
        self.root.protocol("WM_DELETE_WINDOW", self.window_exit)
        
        
        self.selection_top_x = 0
        self.selection_top_y = 0
        self.selection_bottom_x = 0
        self.selection_bottom_y = 0
        self.canvas_for_selection = None
        self.selection_rect = None
        self.root.bind("<Escape>", self.close)         
        self.run()
             
    # Метод запускает:
    # Метод открытие скриншотов;
    # Метод отрисовки меню;
    # Метод захвата фокуса;    
    def run(self):
        self.open_screenshot()
        self.draw_menu()
        self.grab_focuses()

    # Метод отрисовки в программе меню
    def draw_menu(self):
        # Создания плашки меню
        add_new_log("[INFO] - EditorWindow: Отрисовка меню\n")
        menu_bar = Menu(self.root)

        # Создания меню сохранения скриншота в папку и добавление разделителя между другими кнопками
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Сохранить как", command=self.save_screenshot)
        file_menu.add_separator()
        
        # Создания меню копирования скриншота в буфер обмена
        file_menu.add_command(label="Скопировать изображение в буфер обмена", command=self.copy_current_image_to_clipboard)

        # Добавление разделителя и добавления кнопки выхода
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.close)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Создания общего меню для редактирования
        edit_menu = Menu(menu_bar, tearoff=0)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Документация", command=self.help_open)
        help_menu.add_command(label="Логи программы", command=self.log_open)
        

        # Создания меню для меню вращения
        transform_menu = Menu(edit_menu, tearoff=0)

        # Создания меню для вращения скриншота
        rotate_menu = Menu(transform_menu, tearoff=0)
        rotate_menu.add_command(label="Повернуть влево на 90 градусов", command=lambda: self.rotate_current_image(90))
        rotate_menu.add_command(label="Повернуть вправо на 90 градусов", command=lambda: self.rotate_current_image(-90))
        rotate_menu.add_command(label="Повернуть влево на 180 градусов", command=lambda: self.rotate_current_image(180))
        rotate_menu.add_command(label="Повернуть вправо на 180 градусов", command=lambda: self.rotate_current_image(-180))
        transform_menu.add_cascade(label="Поворот", menu=rotate_menu)
        
        # Создания меню для отзеркаливания
        flip_menu = Menu(transform_menu, tearoff=0)
        flip_menu.add_command(label="Отзеркалить горизантально", command=lambda: self.flip_current_image("h"))
        flip_menu.add_command(label="Отзеркалить вертикально", command=lambda: self.flip_current_image("v"))
        transform_menu.add_cascade(label="Отзеркалить", menu=flip_menu)

        # Создания меню для изменения исходного размера скриншота
        resize_menu = Menu(edit_menu, tearoff=0)
        resize_menu.add_command(label="25%", command=lambda: self.resize_val(25))
        resize_menu.add_command(label="50%", command=lambda: self.resize_val(50))
        resize_menu.add_command(label="75%", command=lambda: self.resize_val(75))
        resize_menu.add_command(label="90%", command=lambda: self.resize_val(90))
        resize_menu.add_command(label="100%", command=lambda: self.resize_val(100))
        resize_menu.add_command(label="110%", command=lambda: self.resize_val(110))
        resize_menu.add_command(label="125%", command=lambda: self.resize_val(125))
        transform_menu.add_cascade(label="Масштабирование", menu=resize_menu)

        # Создание меню для фильтров
        filter_menu = Menu(edit_menu, tearoff=0)
        filter_menu.add_command(label="Размытие", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.BLUR))
        filter_menu.add_command(label="Резкость", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.SHARPEN))
        filter_menu.add_command(label="Контур", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.CONTOUR))
        filter_menu.add_command(label="Сглаживание", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.SMOOTH))
        filter_menu.add_command(label="Тиснение", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.EMBOSS))
        filter_menu.add_command(label="Детализация", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.DETAIL))


        # Создание меню для усиления эффектов 
        enhance_menu = Menu(edit_menu, tearoff=0)
        enhance_menu.add_command(label="Насыщенность цвета", command=lambda: self.enhance_current_image("Насыщенность цвета", ImageEnhance.Color))
        enhance_menu.add_command(label="Констрастность", command=lambda: self.enhance_current_image("Контрастность", ImageEnhance.Contrast))
        enhance_menu.add_command(label="Яркость", command=lambda: self.enhance_current_image("Яркость", ImageEnhance.Brightness))
        enhance_menu.add_command(label="Контрастность углов", command=lambda: self.enhance_current_image("Резкость", ImageEnhance.Sharpness))
        enhance_menu.add_separator()
        enhance_menu.add_command(label="Черно-белый", command=lambda: self.convert_current_image("1"))
        enhance_menu.add_command(label="Оттенки серого", command=lambda: self.convert_current_image("L"))
        enhance_menu.add_command(label="Красный", command=lambda: self.convert_current_image("R"))
        enhance_menu.add_command(label="Зеленый", command=lambda: self.convert_current_image("G"))
        enhance_menu.add_command(label="Синий", command=lambda: self.convert_current_image("B"))
        enhance_menu.add_command(label="Инвертировать RGB цвета", command=lambda: self.convert_current_image("roll"))              

        # Добавление новых в меню, в меню edit_menu
        edit_menu.add_cascade(label="Трансформировать", menu=transform_menu)
        edit_menu.add_cascade(label="Фильтры", menu=filter_menu)
        edit_menu.add_cascade(label="Эффекты", menu=enhance_menu)

        menu_bar.add_cascade(label="Редактирование", menu=edit_menu)
        menu_bar.add_cascade(menu=help_menu, label="Помощь")

        # Создание меню для выделения зоны и кропа
        edit_menu.add_command(label="Вырезать", command=self.start_area_selection_of_current_image)

        edit_menu.add_command(label="Отменить изменения", command=lambda: self.return_previous_image())

        # Добавление в root меню
        self.root.configure(menu=menu_bar)
    
    # Метод сохранения скриншота в папку
    def save_screenshot(self):
        new_path = filedialog.asksaveasfilename(initialfile=r"Screenshot.png",
                                                initialdir=f"C:/Users/{os.environ.get("USERNAME")}/Pictures",
                                                filetypes=(("Images", "*.jpg;*.png;*.jpeg;"), ))
        if not new_path:
            return
        try:
            path, ext = new_path.split('.') # Разделение пути сохранения на путь и расширение изображения
            if ext in ["jpg", "png", "jpeg"]: # Проверка что расширение является коректным     
                image = self.photo
                image.save(new_path, ext) # Сохранение скриншота по заданному пути
                add_new_log(f"[INFO] - EditorWindow: Успешное сохранение скриншота {new_path}\n")
                messagebox.showinfo("Ваш скриншот успешно сохранен!", f"Скриншот сохранен по директории: {path}")
            else:
                messagebox.showerror("Ошибка!", f"Неподдерживаемый формат. Поддерживаемый формат: \n.png, \n.jpg, \n.jpeg")
        except ValueError as ex:
            add_new_log(f"[ERROR] - EditorWindow: Неправильное расположение файла {new_path}\n")
            messagebox.showerror("Ошибка!", "Неизвестная ошибка.")    
    
    # Метод отрисовки скриншота на холсте программы      
    def open_screenshot(self):
        add_new_log(f"[INFO] - EditorWindow: Открытие скриншота...\n")
        image_tk = ImageTk.PhotoImage(self.photo)
        self.image_panel = Canvas(self.root, width=image_tk.width(), 
                                  height=image_tk.height(), bd=0, highlightthickness=0) # Создание холста для отрисовки изображения
        self.image_panel.image = image_tk
        add_new_log(f"[INFO] - EditorWindow: Отрисовка скриншота на холсте\n")
        self.image_panel.create_image(0, 0, image=image_tk, anchor="nw") # Запись скриншота в созданный холст
        self.image_panel.pack(expand="yes") # Упаковка холста 

    # Метод забирающий фокус пользователя на редактор
    def grab_focuses(self):
        self.root.grab_set()      
        self.root.focus_set()
        self.root.wait_window()

    def return_previous_image(self):
        if len(self.history_buffer) != 0:
            add_new_log(f"[INFO] - EditorWindow: Возвращение прошлой копии изображения\n")
            self.curSize = self.history_buffer[-1][-1]
            add_new_log(f"[INFO] - EditorWindow: Удален скриншот {self.history_buffer[-1]} из буфера истории\n")
            self.update_image_inside_editor(image=self.history_buffer[-1][0])
            self.history_buffer.pop(-1)

    def add_image_to_history_buffer(self, image):
        if len(self.history_buffer) > 9:
            add_new_log(f"[INFO] - EditorWindow: Очистка буфера истории\n")  
            self.history_buffer.pop(0)

        self.history_buffer.append((image, self.curSize))
        add_new_log(f"[INFO] - EditorWindow: Добавлено изображение в буфер {self.history_buffer[-1]}\n")

    # Метод обновления скриншота на холсте при изменениях   
    def update_image_inside_editor(self, image):
        add_new_log(f"[INFO] - EditorWindow: Обновление изображения на холсте\n")
        self.photo = image
        self.fPhoto = self.resize_current_image() # (нс)
        
        canvas = self.image_panel 

        image_tk = ImageTk.PhotoImage(self.fPhoto)

        add_new_log(f"[INFO] - EditorWindow: Удаления нынешнего изображения холста\n")
        canvas.delete("all")
        canvas.configure(width=image_tk.width(), height=image_tk.height())
        canvas.image = image_tk
        canvas.create_image(0, 0, image=image_tk, anchor="nw")
        add_new_log(f"[INFO] - EditorWindow: Обновлено изображение на холсте\n")     

    # Метод вращения скриншота на n-е колличество градусов
    def rotate_current_image(self, degrees=0):
        image = self.photo
        self.add_image_to_history_buffer(image=image)
        image = image.rotate(degrees, expand=True)
        add_new_log(f"[INFO] - EditorWindow: Изображение было повернуто на {degrees} градусов\n")   

        self.update_image_inside_editor(image)

    # Метод переворачивания скриншота
    def flip_current_image(self, flip_type):
        image = self.photo
        self.add_image_to_history_buffer(image=image)
        if flip_type == "h":
            add_new_log(f"[INFO] - EditorWindow: Изображение было отрезкалено на горизонтали\n") 
            image = ImageOps.mirror(image)
        elif flip_type == "v":
            add_new_log(f"[INFO] - EditorWindow: Изображение было отрезкалено на вертикале\n") 
            image = ImageOps.flip(image)  

        self.update_image_inside_editor(image)        

    # Метод - меняет масштабирование  (нс)
    def resize_current_image(self):
        w, h = self.photo.size
        w = (w * self.curSize) // 100
        h = (h * self.curSize) // 100
        
        if w > 1 or h > 1:
            add_new_log(f"[INFO] - EditorWindow: Изображение было отрезкалено на вертикале\n") 
            return self.photo.resize((w, h))

    # Метод - меняет значение для масштабирования (нс)
    def resize_val(self, percent):
        self.add_image_to_history_buffer(image=self.photo)
        self.curSize = percent
        self.update_image_inside_editor(self.photo)
        add_new_log(f"[INFO] - EditorWindow: Изменение процента масштабирования изображения ({percent})%\n")

    # Метод применения фильторов на скриншот
    def apply_filter_to_current_image(self, filter_type):
        image = self.photo
        self.add_image_to_history_buffer(image=image)

        image = image.filter(filter_type)
        add_new_log(f"[INFO] - EditorWindow: Наложен фильтр {filter_type}\n")
        self.update_image_inside_editor(image)         

    # Метод инициализатор для задачи данных в переменные для выделения
    def start_area_selection_of_current_image(self):
        if self.selection_rect is not None:
            self.canvas_for_selection.delete(self.selection_rect)

        canvas = self.image_panel
        self.canvas_for_selection = canvas
        self.selection_rect = canvas.create_rectangle(self.selection_top_x, self.selection_top_y, self.selection_bottom_x, self.selection_bottom_y, dash=(10, 10), fill="cyan", stipple="gray25", outline="black", width=2)
        print(type(self.canvas_for_selection))

        canvas.bind("<Button-1>",self.get_selection_start_post)
        canvas.bind("<B1-Motion>", self.update_selection_end_pos)
        canvas.bind("<ButtonRelease-1>", self.crop_current_image)

    # Метод фиксирующий начальный кординаты выделения
    def get_selection_start_post(self, event):
        self.selection_top_x, self.selection_top_y = event.x, event.y
        add_new_log(f"[INFO] - EditorWindow: Начало выделения области для обрезки [{self.selection_top_x},{self.selection_top_y}]\n")
    
    # Метод обновления данных для выделения кропа 
    def update_selection_end_pos(self, event):
        self.selection_bottom_x, self.selection_bottom_y = event.x, event.y
        add_new_log(f"[INFO] - EditorWindow: Продолжение выделения области для обрезки [{self.selection_bottom_x},{self.selection_bottom_y}]\n")
        if self.canvas_for_selection is not None and self.selection_rect is not None:
            self.canvas_for_selection.coords(self.selection_rect, self.selection_top_x, self.selection_top_y, self.selection_bottom_x, self.selection_bottom_y)

    # Метод выделения зоны и кнопка изображения
    def crop_current_image(self, event):
        self.canvas_for_selection.unbind("<Button-1>") #Начало выделения
        self.canvas_for_selection.unbind("<B1-Motion>") #Создание выделения
        self.canvas_for_selection.unbind("<ButtonRelease-1>") #Остановка выделения

        self.canvas_for_selection.delete(self.selection_rect) # Удаление выделения
        image = self.photo
        self.add_image_to_history_buffer(image=image)

        if self.selection_top_x + 50 > self.selection_bottom_x or self.selection_top_y + 50 > self.selection_bottom_y:
            self.crop_data_reset()
            add_new_log(f"[ERROR] - EditorWindow: Выделенная область слишком маленькая\n")
            return 

        image = image.crop((self.selection_top_x, self.selection_top_y, self.selection_bottom_x, self.selection_bottom_y))
        add_new_log(f"[INFO] - EditorWindow: Обрезка изображения по кординатам {self.selection_top_x},{self.selection_top_y},{self.selection_bottom_x},{self.selection_bottom_y}\n")
        self.crop_data_reset()
        self.update_image_inside_editor(image)

    # Метод конвертации изображения
    def convert_current_image(self, mode):
        image = self.photo
        self.add_image_to_history_buffer(image=image)

        # Инвертирование цветом RGB
        if mode == "roll":
            if image.mode != "RGB":
                add_new_log(f"[EditorWindow][ОШИБКА] Изображение не формата RGB\n")
                messagebox.showerror("Ошибка", f"Не удается прокрутить картинку без RGB мода '{image.mode}'")
                return
            
            image = Image.fromarray(np.array(image)[:,:,::-1])
            add_new_log(f"[INFO] - EditorWindow: Инвертирования цветов изображения\n")
            self.update_image_inside_editor(image)
            return
        
        # Выделение одного цвета на скриншоте
        elif mode in "R G B".split(' '):
            if image.mode != "RGB":
                add_new_log(f"[ERROR] - EditorWindow: Изображение не формата RGB\n") 
                messagebox.showerror("RGB Roll error", f"Неизвестная ошибка! '{image.mode}'")
                return
            
            a = np.array(image)
            a[:,:,(mode!="R", mode!="G", mode!="B")] *= 0
            image = Image.fromarray(a)
            add_new_log(f"[INFO] - EditorWindow: Выделение {mode} цвета на изображение\n")
            self.update_image_inside_editor(image)
            return

        try:
            image = image.convert(mode)
            self.update_image_inside_editor(image)
        except ValueError as ex:
            add_new_log(f"[ERROR] - EditorWindow: {ex}\n") 
            messagebox.showerror("Ошибка", f"Неизвестная ошибка! '{ex}'")    

    # Усиление эффектов на скриншоте
    def enhance_current_image(self, name, enhance):
        image = self.photo
        self.add_image_to_history_buffer(image=image)
        add_new_log(f"[INFO] - EditorWindow: Запуск настройки эффектов класса EnhanceSliderWindow\n")
        EnhanceSliderWindow(root=self.root, name=name, enhance=enhance,
                            image=image, update_method=self.update_image_inside_editor)

    # Метод копирования скриншота в буфер обмена
    def copy_current_image_to_clipboard(self):
        copy_image_to_clipboard(self.photo)
        add_new_log(f"[INFO] - EditorWindow: Копирование изображения в буфер обмена\n")
        messagebox.showinfo("Скриншот скопирован!", "Скриншот был успешно скопирован в буфер обмена!")

    def crop_data_reset(self):
        self.selection_rect = None
        self.canvas_for_selection = None
        self.selection_top_x, self.selection_top_y = 0, 0
        self.selection_bottom_x, self.selection_bottom_y = 0, 0
    
    def help_open(self):
        add_new_log(f"[INFO] - EditorWindow: Открытие документации пользователя\n")
        os.startfile(f"{self.dir}\\help_doc.docx")

    def log_open(self):
        os.startfile(f"{self.dir}\\log.txt")

    def window_exit(self):
        close = messagebox.askyesno("Выйти?", "Вы уверена что вы хотите выйти?")
        if close:
            self.close()

    # Метод выхода из редактора и очистки памяти
    def close(self, event=None):
        add_new_log(f"[INFO] - EditorWindow: Закрытие редактора\n")
        self.history_buffer = None
        self.photo = None
        self.fPhoto = None
        self.root.destroy()
