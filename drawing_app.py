import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
from typing import List


class DrawingApp:
    def __init__(self, root: tk.Tk) -> None:
        """
        Конструктор класса DrawingApp. Инициализирует интерфейс приложения,
        создает холст для рисования и задает начальные настройки.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Создание изображения и инструмента для рисования
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создание холста в интерфейсе
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Инициализация пользовательского интерфейса
        self.setup_ui()

        # Переменные для рисования
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1  # Начальный размер кисти

        # Привязка событий мыши
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self) -> None:
        """
        Создает элементы управления (кнопки, выпадающий список и слайдер)
        для настройки приложения.
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
            command=lambda value: self.update_brush_size(value)  # Обновляем размер кисти
        )
        self.brush_size_scale.pack(side=tk.LEFT)

        # Выпадающий список для выбора размера кисти
        sizes = [1, 2, 5, 10]  # Предопределенные размеры кисти
        self.brush_size_var = tk.IntVar(value=sizes[0])  # Переменная для хранения текущего размера кисти
        size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        size_menu.pack(side=tk.LEFT)
        size_menu.config(width=10)  # Устанавливаем ширину меню

    def update_brush_size(self, size: int) -> None:
        """
        Обновляет текущий размер кисти при выборе из выпадающего списка или слайдера.

        :param size: Новый размер кисти, выбранный пользователем.
        """
        self.brush_size = int(size)  # Обновляем текущий размер кисти

    def paint(self, event: tk.Event) -> None:
        """
        Рисует линию на холсте при движении мыши.

        :param event: Событие, связанное с движением мыши.
        """
        if self.last_x and self.last_y:
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

    def reset(self, event: tk.Event) -> None:
        """
        Сбрасывает координаты кисти после завершения рисования.

        :param event: Событие завершения рисования (отпускание кнопки мыши).
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self) -> None:
        """
        Очищает холст и создает новое изображение.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self) -> None:
        """
        Открывает диалоговое окно для выбора цвета кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self) -> None:
        """
        Сохраняет текущее изображение в формате PNG.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main() -> None:
    """
    Главная функция запуска приложения.
    """
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()