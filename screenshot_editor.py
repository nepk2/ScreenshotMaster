from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
import pyautogui as pag
import numpy as np
import os


from сlipboard_buffer import copy_image_to_clipboard
from screenshot_enhancer import EnhanceSliderWindow


class EditorWindow:
    def __init__(self, parent, screenshot):
        self.root = Toplevel(parent) # Создание дочернего окна от основной программы
        self.root.title("SSM Editor")
        self.root.iconbitmap(r"Diplom/icons/SSM Editor.ico")        
        self.photo = screenshot # Запись скриншота в переменную
        self.history_buffer = []
        self.root.protocol("WM_DELETE_WINDOW", self.window_exit)
        #self._image = None

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
        flip_menu = Menu(edit_menu, tearoff=0)
        flip_menu.add_command(label="Отзеркалить горизантально", command=lambda: self.flip_current_image("h"))
        flip_menu.add_command(label="Отзеркалить вертикально", command=lambda: self.flip_current_image("v"))

        # Создания меню для изменения исходного размера скриншота
        resize_menu = Menu(edit_menu, tearoff=0)
        resize_menu.add_command(label="25%", command=lambda: self.resize_current_image(25))
        resize_menu.add_command(label="50%", command=lambda: self.resize_current_image(50))
        resize_menu.add_command(label="75%", command=lambda: self.resize_current_image(75))
        resize_menu.add_command(label="90%", command=lambda: self.resize_current_image(90))
        resize_menu.add_command(label="110%", command=lambda: self.resize_current_image(110))
        resize_menu.add_command(label="125%", command=lambda: self.resize_current_image(125))

        # Создание меню для фильтров
        filter_menu = Menu(edit_menu, tearoff=0)
        filter_menu.add_command(label="Размытие", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.BLUR))
        filter_menu.add_command(label="Резкость", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.SHARPEN))
        filter_menu.add_command(label="Контур", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.CONTOUR))
        filter_menu.add_command(label="Сглаживание", command=lambda: self.apply_filter_to_current_image(filter_type=ImageFilter.SMOOTH))

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
        edit_menu.add_cascade(label="Отзеркалить", menu=flip_menu)
        edit_menu.add_cascade(label="Изменить размер", menu=resize_menu)
        edit_menu.add_cascade(label="Фильтры", menu=filter_menu)
        edit_menu.add_cascade(label="Эффекты", menu=enhance_menu)
        menu_bar.add_cascade(label="Редактирование", menu=edit_menu)

        # Создание меню для выделения зоны и кропа
        edit_menu.add_command(label="Вырезать", command=self.start_area_selection_of_current_image)

        edit_menu.add_command(label="Отменить изменения", command=lambda: self.return_previous_image())

        # Добавление в root меню
        self.root.configure(menu=menu_bar)
    
    # Метод сохранения скриншота в папку
    def save_screenshot(self):
        new_path = filedialog.asksaveasfilename(initialfile=r"Screenshot.png", initialdir=f"C:/Users/{os.environ.get("USERNAME")}/Pictures", filetypes=(("Images", "*.jpg;*.png;*.jpeg;"), ))
        if not new_path:
            return
        try:
            path, ext = new_path.split('.') # Разделение пути сохранения на путь и расширение изображения
            if ext in ["jpg", "png", "jpeg"]: # Проверка что расширение является коректным     
                image = self.photo
                image.save(new_path, ext) # Сохранение скриншота по заданному пути
                messagebox.showinfo("Ваш скриншот успешно сохранен!", f"Скриншот сохранен по директории: {path}")
            else:
                messagebox.showerror("Ошибка!", f"Неподдерживаемый формат. Поддерживаемый формат: \n.png, \n.jpg, \n.jpeg")
        except ValueError as ex:
            messagebox.showerror("Ошибка!", "Неизвестная ошибка.")    
    
    # Метод отрисовки скриншота на холсте программы      
    def open_screenshot(self):
        image_tk = ImageTk.PhotoImage(self.photo)
        self.image_panel = Canvas(self.root, width=image_tk.width(), height=image_tk.height(), bd=0, highlightthickness=0) # Создание холста для отрисовки изображения
        self.image_panel.image = image_tk
        self.image_panel.create_image(0, 0, image=image_tk, anchor="nw") # Запись скриншота в созданный холст
        self.image_panel.pack(expand="yes") # Упаковка холста 

    # Метод забирающий фокус пользователя на редактор
    def grab_focuses(self):
        self.root.grab_set()      
        self.root.focus_set()
        self.root.wait_window()

    def return_previous_image(self):
        if len(self.history_buffer) != 0:
            self.update_image_inside_editor(image=self.history_buffer[-1])
            self.history_buffer.pop(-1)

    def add_image_to_history_buffer(self, image):
        if len(self.history_buffer) > 9:  
            self.history_buffer.pop(0)

        self.history_buffer.append(image)

    # Метод обновления скриншота на холсте при изменениях   
    def update_image_inside_editor(self, image):
        self.photo = image

        canvas = self.image_panel

        image_tk = ImageTk.PhotoImage(image)

        canvas.delete("all")
        canvas.configure(width=image_tk.width(), height=image_tk.height())
        canvas.image = image_tk
        canvas.create_image(0, 0, image=image_tk, anchor="nw")        

    # Метод вращения скриншота на n-е колличество градусов
    def rotate_current_image(self, degrees=0):
        image = self.photo
        self.add_image_to_history_buffer(image=image)
        image = image.rotate(degrees, expand=True)

        self.update_image_inside_editor(image)

    # Метод переворачивания скриншота
    def flip_current_image(self, flip_type):
        image = self.photo
        self.add_image_to_history_buffer(image=image)
        if flip_type == "h":
            image = ImageOps.mirror(image)
        elif flip_type == "v":
            image = ImageOps.flip(image)  

        self.update_image_inside_editor(image)        

    # Метод изменения размера исходного размера скриншота  
    def resize_current_image(self, percent):
        image = self.photo
        self.add_image_to_history_buffer(image=image)

        w, h = image.size
        w = (w * percent) // 100
        h = (h * percent) // 100

        image = image.resize((w, h))
        self.update_image_inside_editor(image)
        image = None   

    # Метод применения фильторов на скриншот
    def apply_filter_to_current_image(self, filter_type):
        image = self.photo
        self.add_image_to_history_buffer(image=image)

        image = image.filter(filter_type)
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
    
    # Метод обновления данных для выделения кропа 
    def update_selection_end_pos(self, event):
        self.selection_bottom_x, self.selection_bottom_y = event.x, event.y
        if self.canvas_for_selection is not None and self.selection_rect is not None:
            self.canvas_for_selection.coords(self.selection_rect, self.selection_top_x, self.selection_top_y, self.selection_bottom_x, self.selection_bottom_y)

    # Метод выделения зоны и кнопка изображения
    def crop_current_image(self, event):
        self.canvas_for_selection.unbind("<Button-1>")
        self.canvas_for_selection.unbind("<B1-Motion>")
        self.canvas_for_selection.unbind("<ButtonRelease-1>")

        self.canvas_for_selection.delete(self.selection_rect)
        image = self.photo
        self.add_image_to_history_buffer(image=image)

        if self.selection_top_x + 50 > self.selection_bottom_x or self.selection_top_y + 50 > self.selection_bottom_y:
            self.crop_data_reset()
            return 

        image = image.crop((self.selection_top_x, self.selection_top_y, self.selection_bottom_x, self.selection_bottom_y))
        self.crop_data_reset()
        self.update_image_inside_editor(image)

    # Метод конвертации изображения
    def convert_current_image(self, mode):
        image = self.photo
        self.add_image_to_history_buffer(image=image)

        # Инвертирование цветом RGB
        if mode == "roll":
            if image.mode != "RGB":
                messagebox.showerror("Ошибка", f"Не удается прокрутить картинку без RGB мода '{image.mode}'")
                return
            
            image = Image.fromarray(np.array(image)[:,:,::-1])
            self.update_image_inside_editor(image)
            return
        
        # Выделение одного цвета на скриншоте
        elif mode in "R G B".split(' '):
            if image.mode != "RGB": 
                messagebox.showerror("RGB Roll error", f"Неизвестная ошибка! '{image.mode}'")
                return
            
            a = np.array(image)
            a[:,:,(mode!="R", mode!="G", mode!="B")] *= 0
            image = Image.fromarray(a)
            self.update_image_inside_editor(image)
            return

        try:
            image = image.convert(mode)
            self.update_image_inside_editor(image)
        except ValueError as ex:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка! '{ex}'")    

    # Усиление эффектов на скриншоте
    def enhance_current_image(self, name, enhance):
        image = self.photo
        self.add_image_to_history_buffer(image=image)
        EnhanceSliderWindow(root=self.root, name=name, enhance=enhance, image=image, update_method=self.update_image_inside_editor)

    # Метод копирования скриншота в буфер обмена
    def copy_current_image_to_clipboard(self):
        copy_image_to_clipboard(self.photo)
        messagebox.showinfo("Скриншот скопирован!", "Скриншот был успешно скопирован в буфер обмена!")

    def crop_data_reset(self):
        self.selection_rect = None
        self.canvas_for_selection = None
        self.selection_top_x, self.selection_top_y = 0, 0
        self.selection_bottom_x, self.selection_bottom_y = 0, 0
    
    def window_exit(self):
        close = messagebox.askyesno("Выйти?", "Вы уверена что вы хотите выйти?")
        if close:
            self.close()

    # Метод выхода из редактора и очистки памяти
    def close(self, event=None):
        self.history_buffer = None
        self.photo = None
        self.root.destroy()
