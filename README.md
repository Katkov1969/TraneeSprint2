ЗАДАНИЕ 1
Объяснение изменений:
1. Добавлен выпадающий список tk.OptionMenu:
Список предопределенных размеров кисти sizes = [1, 2, 5, 10].
Используется переменная self.brush_size_var для хранения текущего значения из списка.
При выборе значения из меню вызывается метод update_brush_size, который обновляет текущий размер кисти.
2. Добавлен метод update_brush_size:
Синхронизирует выпадающий список с слайдером, чтобы изменения в одном элементе отображались на другом.
Выпадающий список и слайдер работают независимо, но синхронизированы. Например, если пользователь выбрал размер через список, значение слайдера обновляется автоматически.
3. Внесены изменения в метод paint.
Теперь вместо значения слайдера (self.brush_size_scale.get()) используется переменная self.brush_size, которая обновляется как слайдером, так и выпадающим списком.
4. В методе setup_ui добавлен обработчик события изменения значения слайдера.
Теперь при изменении значения слайдера будет вызываться метод update_brush_size, который обновляет переменную self.brush_size.

Пример работы:
![Смена размера кисти](https://github.com/user-attachments/assets/8f2c919b-fe7a-44bb-b1e3-d7a903709e05)

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 2
Объяснене изменений:
1. В метод setup_ui добавлена кнопка "Ластик". Кнопка вызывает метод use_eraser, который переключает инструмент на ластик.
2. В класс DrawingApp добавлен новый метод use_eraser. Если текущий цвет кисти не белый, сохраняется текущий цвет в self.previous_color, а self.pen_color устанавливается в белый.
Если текущий цвет уже белый (инструмент "Ластик" активен), то восстанавливается предыдущий цвет кисти.
3.Обновление метода choose_color: При выборе нового цвета кисти он сохраняется в self.previous_color. Это нужно для восстановления цвета кисти после использования ластика.

Логика работы:
1. После нажатия кнопки "Ластик" текущий цвет кисти (self.pen_color) переключается на белый ("white"), а предыдущий цвет кисти сохраняется в переменную self.previous_color.
2. Если пользователь снова нажимает кнопку "Ластик", инструмент переключается обратно на кисть с сохраненным цветом.
3. При выборе нового цвета через кнопку "Выбрать цвет", он сохраняется в self.previous_color.

Пример работы:
![Добавление ластика](https://github.com/user-attachments/assets/90b4e884-ed65-44a3-a9c1-d623af25bae1)

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 3
Объяснение изменений:
1.Добавлена строка в конструкторе. Теперь правая кнопка мыши вызывает метод pick_color.
2.Добавлен новый метод pick_color для инструмента "Пипетка".
3. Добавлен метод update_color_label. Обновление цвета метки после действий. После изменения цвета кисти (как в функциях choose_color, use_eraser или pick_color), метка обновляется с помощью нового метода update_color_label.

Логика работы:
При клике правой кнопкой мыши (<Button-3>):
1. Программа получает координаты клика (event.x, event.y).
2. С помощью метода getpixel из библиотеки Pillow программа извлекает цвет пикселя на изображении, соответствующего этим координатам.
3. Цвет преобразуется из RGB в HEX (например, (255, 0, 0) → #ff0000). Этот цвет устанавливается как текущий цвет кисти (self.pen_color).
4. Метка color_label также обновляется, чтобы отразить новый цвет.
Если пользователь кликает за пределами холста (например, на границе окна), программа обрабатывает это с помощью исключения (IndexError) и выводит предупреждение:"Ошибка", "Клик вне области рисунка!"
 
В консоли выводится цвет пикселя, на котором произошел клик правой кнопкой мыши.

Пример работы:
Рисунок:
![Пипетка](https://github.com/user-attachments/assets/c60dcd66-dc7f-4aef-8899-e9b6b5357c78)

Вывод в консоль:
![Консоль при выборе цвета пипетки](https://github.com/user-attachments/assets/d697f54c-0b78-4937-b5b0-d0363ed7886f)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 4
Изменения в коде:
1. В методе __init__ добавлены следующие привязки:
    self.root.bind('<Control-s>', self.save_image)  - Сохранение изображения
    self.root.bind('<Control-c>', self.choose_color) - Выбор цвета кисти

2. Обновлены функций save_image и choose_color
Теперь эти функции принимают необязательный аргумент event (событие клавиши). Это необходимо для работы с горячими клавишами, так как привязанные функции в bind автоматически получают объект события:
def save_image(self, event=None) -> None:
def choose_color(self, event=None) -> None:

Логика работы добавленных функций:
Когда пользователь нажимает Ctrl+S, вызывается функция save_image. Она открывает окно для выбора пути сохранения изображения и сохраняет текущий холст в формате PNG.
Когда пользователь нажимает Ctrl+C, вызывается функция choose_color. Она открывает окно выбора цвета, где пользователь может выбрать новый цвет кисти.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 5
Изменения в коде:
1.В метод setup_ui добавлен новый виджет self.preview_canvas

2. Добавлен метод update_color_preview, который обновляет фон виджета self.preview_canvas при изменении цвета кисти.

3.Обновление предварительного просмотра после изменения цвета:
 В функциях, изменяющих цвет кисти:
choose_color
use_eraser
pick_color 
вызывается self.update_color_preview().

Пример выполнения:
![Предварительный просмотр цвета кисти](https://github.com/user-attachments/assets/b8eb806b-0939-4917-9244-317e8c7a3f20)

+++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 6
Изменения в коде:
1. Из tkinter импортируется simpledialog.

2. В методе setup_ui добавлена кнопка Изменить размер холста:
     resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
     resize_button.pack(side=tk.LEFT, padx=5)

3. Добавлен новый метод resize_canvas
      Этот метод открывает два диалоговых окна (simpledialog.askinteger) для ввода новой ширины и высоты холста.
      Создается новый объект Image с указанными размерами, и старое изображение копируется на новый холст.
      После изменения размеров обновляются параметры self.canvas_width и self.canvas_height, а также свойства Tkinter-холста.
Пример выполненния:
![Изменения размеров холста](https://github.com/user-attachments/assets/8d5f638f-a7ec-4d9f-bd37-56fe844a1486)

+++++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 7
Изменения в коде:
1. В конструктор __init__ добавлено:
    - Нновый атрибут self.text_mode
    - Изменена привязка событий мыши в конструкторе. Теперь при клике левой кнопкой мыши вызывается метод add_text, если активен режим текста.
    - Добавлен новый атрибут self.canvas_bg_color. Этот атрибут хранит текущий цвет фона холста.

2.  В метод setup_ui добавлена кнопка "Текст". Эта кнопка вызывает метод activate_text_mode, который включает режим текста.

3. Добавлен новый метод  activate_text_mode
    Этот метод активирует режим текста и уведомляет пользователя, что теперь можно добавить текст на холст.

4. Добавлен новый метод add_text.
    Этот метод:
     - Проверяет, активен ли режим текста.
     - Открывает окно для ввода текста с помощью tk.simpledialog.askstring.
     - Рисует текст на изображении с помощью ImageDraw.text.
     - Выходит из режима текста после добавления текста.

5. В метод setup_ui добавлена кнопка "Изменить фон".

6. Добавлен новый метод change_background_color. 
Этот метод:
     - Открывает окно выбора цвета с помощью colorchooser.askcolor.
     - Устанавливает новый цвет для фона холста.
     - Сбрасывает изображение, вызывая метод clear_canvas.

7. Внесены изменения в методе clear_canvas.
    Теперь фон нового изображения создается с использованием текущего цвета фона self.canvas_bg_color.

8. Внесены изменения в методе use_eraser. Ластик теперь использует текущий цвет фона (self.canvas_bg_color), чтобы "стирать" рисунок.

Прмеры работы программы:
1. Вызов окна ввода текста:
   ![Вызов окна ввода текста](https://github.com/user-attachments/assets/14502bed-f539-4dd2-b2b1-1ebf59484df4)
2. Окно ввода текста:
   ![Окно ввода текста](https://github.com/user-attachments/assets/c3ace403-a26b-4928-ba65-dc978b0928c8)
3. Введенный текст:
   ![Введенный текст](https://github.com/user-attachments/assets/a0507463-9f3d-46e0-bf82-66ebb1351829)
















