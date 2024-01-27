import csv
from tkinter import Tk, Button, filedialog
from app.ErrorWindow import ErrorWindow
from app import config
from app.GraphWindow import GraphWindow
from app.Utils import add_settings


@add_settings("Визуализация триангуляционных данных")
class MainApp(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        button_load = Button(self, text="Выбрать файл", padx=150, pady=20, command=lambda: self.load_file())

        button_visual = Button(self, text='Визуализация', padx=150, pady=20, command=lambda: self.create_visualization())

        button_exit = Button(self, text='Выход', padx=150, pady=20, command=lambda: self.destroy())
        # Располагаем кнопки на экране

        button_load.grid(row=0, column=0, pady=(5, 0), padx=(2, 0))
        button_visual.grid(row=1, column=0, pady=(5, 0), padx=(2, 0))
        button_exit.grid(row=2, column=0, pady=(5, 0), padx=(2, 0))

    def load_file(self):
        # Загрузка csv
        filepath = filedialog.askopenfilename()
        if filepath != "":
            config.data = []
            with open(filepath, encoding='utf-8') as r_file:
                # Создаем объект reader, указываем символ-разделитель ","
                file_reader = csv.reader(r_file, delimiter=",")
                # Счетчик для подсчета количества строк и вывода заголовков столбцов
                count = 0
                # Считывание данных из CSV файла
                for row in file_reader:
                    if count == 0:
                        # Проверка количества и содержания столбцов
                        if len(row) != 3:
                            ErrorWindow(self, config.errorTextImport)
                            break
                    else:
                        l = []
                        for num in row:
                            l.append(int(num))
                        config.data.append(l)
                    count += 1
        else:
            ErrorWindow(self, config.errorTextImport)

    def create_visualization(self):
        gW = GraphWindow()
        gW.mainloop()