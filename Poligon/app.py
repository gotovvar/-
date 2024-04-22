import tkinter as tk
from tkinter import filedialog, messagebox
from algorithms import sorty_graham, sorty_jarvis


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Poligon")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, width=800, height=550, bg='white')
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.grid(row=1, column=0, sticky='ns')

        self.load_button = tk.Button(self.sidebar, text="Загрузить из файла", command=self.load_from_file)
        self.load_button.pack(pady=10)

        self.algorithm = "Грэхам"
        self.points = []

        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)
        self.segmentMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.segmentMenu.add_command(label="Грэхам", command=lambda: self.set_algorithm("Грэхам"))
        self.segmentMenu.add_command(label="Джарвис", command=lambda: self.set_algorithm("Джарвис"))
        self.mainMenu.add_cascade(label="Алгоритм", menu=self.segmentMenu)

    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    points = [tuple(map(float, line.strip().split())) for line in file]
                    if self.algorithm == "Грэхам":
                        self.create_graham(points)
                    else:
                        self.create_jarvis(points)
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def delay(self, x, y):
        self.canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill='black')

    def zero(self):
        self.canvas.create_rectangle(0, 0, 1920, 1080, fill='white')

    def create_graham(self, start_points):
        self.canvas.delete("all")

        points = sorty_graham(start_points)
        p = start_points
        for point in p:
            self.delay(point[0], point[1])
        for point in points:
            self.canvas.create_rectangle(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, outline='red',
                                         fill='red')

        segments = []
        for i in range(len(points)):
            segment = []
            if i == 0:
                segment.append(points[len(points) - 1])
                segment.append(points[i])
            else:
                segment.append(points[i - 1])
                segment.append(points[i])
            segments.append(segment)

        for segment in segments:
            self.after(100, self.canvas.create_line(segment[0][0], segment[0][1], segment[1][0], segment[1][1]))

    def create_jarvis(self, start_points):
        self.canvas.delete("all")

        points = sorty_jarvis(start_points)
        points.remove(points[len(points) - 1])
        p = start_points
        for point in p:
            self.delay(point[0], point[1])
        for point in points:
            self.canvas.create_rectangle(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, outline='red', fill='red')
            self.update()

        segments = []
        for i in range(len(points)):
            segment = []
            if i == 0:
                segment.append(points[len(points) - 1])
                segment.append(points[i])
            else:
                segment.append(points[i - 1])
                segment.append(points[i])
            segments.append(segment)

        for segment in segments:
            self.after(100, self.canvas.create_line(segment[0][0], segment[0][1], segment[1][0], segment[1][1]))
            self.update()
