import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk


class DrawingApp:
    def __init__(self, root: tk.Tk) -> None:
        """
        Конструктор класса DrawingApp. Инициализирует интерфейс приложения,
        создает холст для рисования и задает начальные настройки.
        """
        self.root = root
        self.root.title("Рисовалка с пипеткой")

        # Переменные для рисования
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'  # Текущий цвет кисти
        self.previous_color = self.pen_color  # Предыдущий цвет кисти для восстановления после ластика
        self.brush_size = 1  # Начальный размер кисти
        self.text_mode = False  # Режим ввода текста

        # Размеры холста
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas_bg_color = "white"  # Цвет фона холста

        # Создание изображения и инструмента для рисования
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.canvas_bg_color)
        self.draw = ImageDraw.Draw(self.image)

        # Создание холста Tkinter
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Переменная для хранения изображения Tkinter
        self.canvas_image = None

        # Инициализация пользовательского интерфейса
        self.setup_ui()

        # Привязка событий мыши
        self.canvas.bind('<B1-Motion>', self.paint)  # ЛКМ для рисования
        self.canvas.bind('<ButtonRelease-1>', self.reset)  # Сброс координат
        self.canvas.bind('<Button-3>', self.pick_color)  # ПКМ для выбора цвета пипеткой
        self.canvas.bind('<Button-1>', self.add_text)  # ЛКМ для установки текста

        # Привязка горячих клавиш
        self.root.bind('<Control-s>', self.save_image)  # Сохранение изображения
        self.root.bind('<Control-c>', self.choose_color)  # Выбор цвета кисти

        # Инициализируем изображение на холсте
        self.update_canvas()

    def setup_ui(self) -> None:
        """
        Создает элементы управления (кнопки и слайдеры) для настройки приложения.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Кнопка очистки холста
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Кнопка выбора цвета
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Кнопка сохранения изображения
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Слайдер для изменения размера кисти
        self.brush_size_scale = tk.Scale(
            control_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="Размер кисти",
            command=lambda value: self.update_brush_size(value)
        )
        self.brush_size_scale.pack(side=tk.LEFT)

        # Кнопка "Ластик"
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Кнопка для добавления текста
        text_button = tk.Button(control_frame, text="Текст", command=self.activate_text_mode)
        text_button.pack(side=tk.LEFT)

        # Кнопка изменения цвета фона
        bg_color_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background_color)
        bg_color_button.pack(side=tk.LEFT)

        # Метка для отображения текущего цвета кисти
        self.color_label = tk.Label(control_frame, text="Цвет кисти", bg=self.pen_color, width=10)
        self.color_label.pack(side=tk.LEFT)

        # Маленький холст для предварительного просмотра цвета кисти
        self.preview_canvas = tk.Canvas(control_frame, width=30, height=30, bg=self.pen_color, bd=2, relief=tk.SUNKEN)
        self.preview_canvas.pack(side=tk.LEFT)

        # Кнопка изменения размера холста
        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT, padx=5)

    def update_brush_size(self, size: int) -> None:
        """
        Обновляет текущий размер кисти при изменении значения слайдера.
        """
        self.brush_size = int(size)

    def paint(self, event: tk.Event) -> None:
        """
        Рисует линию на холсте при движении мыши.
        """
        if self.last_x is not None and self.last_y is not None:
            # Рисуем линию на холсте Tkinter
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.brush_size, fill=self.pen_color,
                capstyle=tk.ROUND, smooth=tk.TRUE
            )
            # Рисуем линию на изображении Pillow
            self.draw.line(
                [self.last_x, self.last_y, event.x, event.y],
                fill=self.pen_color, width=self.brush_size
            )

        self.last_x = event.x
        self.last_y = event.y

        # Обновляем отображение изображения на холсте
        self.update_canvas()

    def reset(self, event: tk.Event) -> None:
        """
        Сбрасывает координаты кисти после завершения рисования.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self) -> None:
        """
        Очищает холст и создает новое изображение.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.canvas_bg_color)
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas()

    def choose_color(self, event=None) -> None:
        """
        Открывает диалоговое окно для выбора цвета кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.previous_color = self.pen_color  # Сохраняем выбранный цвет кисти
        #self.update_color_label()
        self.update_color_preview()

    def use_eraser(self) -> None:
        """
        Переключает инструмент на ластик, устанавливая цвет кисти в цвет фона.
        """
        if self.pen_color != self.canvas_bg_color:
            self.previous_color = self.pen_color
            self.pen_color = self.canvas_bg_color
        else:
            self.pen_color = self.previous_color
        self.update_color_preview()


    def activate_text_mode(self) -> None:
        """
        Активирует режим текста.
        """
        self.text_mode = True
        messagebox.showinfo("Информация", "Нажмите на холст, чтобы добавить текст.")

    def add_text(self, event: tk.Event) -> None:
        """
        Добавляет текст на холст в указанной точке.
        """
        if not self.text_mode:
            return

        text = simpledialog.askstring("Введите текст", "Введите текст для добавления:")
        if text:
            # Рисуем текст на изображении Pillow
            self.draw.text((event.x, event.y), text, fill=self.pen_color)
            # Обновляем холст
            self.update_canvas()

        # Выходим из режима текста
        self.text_mode = False

    def change_background_color(self) -> None:
        """
        Изменяет цвет фона холста.
        """
        new_color = colorchooser.askcolor(color=self.canvas_bg_color)[1]
        if new_color:
            self.canvas_bg_color = new_color
            self.canvas.config(bg=self.canvas_bg_color)
            self.clear_canvas()  # Очищаем холст (сбрасываем изображение)

    def pick_color(self, event: tk.Event) -> None:
        """
        Инструмент "Пипетка". Устанавливает цвет кисти в цвет пикселя под правым кликом мыши.
        """
        # Координаты клика
        x, y = event.x, event.y

        try:
            # Получаем цвет пикселя из изображения
            color = self.image.getpixel((x, y))
            # Преобразуем RGB в HEX
            self.pen_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            self.previous_color = self.pen_color

            # Обновляем метку цвета
            # self.update_color_label()
            self.update_color_preview()

            # Выводим информацию для отладки
            print(f"Выбран цвет: {self.pen_color}")
        except IndexError:
            # Если клик за пределами изображения
            messagebox.showwarning("Ошибка", "Клик вне области рисунка!")

    def update_color_label(self) -> None:
        """
        Обновляет метку текущего цвета кисти в интерфейсе.
        """
        self.color_label.config(bg=self.pen_color)

    def update_color_preview(self) -> None:
        """
        Обновляет предварительный просмотр текущего цвета кисти.
        """
        self.preview_canvas.config(bg=self.pen_color)

    def save_image(self, event=None) -> None:
        """
        Сохраняет текущее изображение в формате PNG.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_canvas(self) -> None:
        """
        Синхронизирует изображение Pillow с холстом Tkinter.
        """
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)

    def resize_canvas(self) -> None:
        """
        Изменяет размер холста на основе пользовательского ввода.
        """
        new_width = simpledialog.askinteger("Изменить ширину", "Введите новую ширину:", minvalue=100, maxvalue=2000)
        new_height = simpledialog.askinteger("Изменить высоту", "Введите новую высоту:", minvalue=100, maxvalue=2000)

        if new_width and new_height:
            self.canvas_width = new_width
            self.canvas_height = new_height

            # Обновляем размер холста Tkinter
            self.canvas.config(width=self.canvas_width, height=self.canvas_height)

            # Создаем новое изображение Pillow с новыми размерами
            new_image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            new_image.paste(self.image, (0, 0))  # Копируем старые данные на новый холст
            self.image = new_image
            self.draw = ImageDraw.Draw(self.image)

            # Обновляем холст
            self.update_canvas()


def main() -> None:
    """
    Главная функция запуска приложения.
    """
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма была прервана пользователем.")