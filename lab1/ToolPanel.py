import tkinter as tk


class ToolPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.algorithm = "dda"

        self.line_menu = tk.Menu(self.master, tearoff=0)
        self.line_menu.add_command(label="ЦДА", command=lambda: self.set_algorithm("dda"))
        self.line_menu.add_command(label="Брезенхем", command=lambda: self.set_algorithm("bresenham"))
        self.line_menu.add_command(label="Ву", command=lambda: self.set_algorithm("wu"))

        self.second_order_line_menu = tk.Menu(self.master, tearoff=0)
        self.second_order_line_menu.add_command(label="Окружность", command=lambda: self.set_algorithm("circle"))
        self.second_order_line_menu.add_command(label="Эллипс", command=lambda: self.set_algorithm("ellipse"))
        self.second_order_line_menu.add_command(label="Гипербола", command=lambda: self.set_algorithm("hyperbola"))
        self.second_order_line_menu.add_command(label="Парабола", command=lambda: self.set_algorithm("parabola"))

        self.parametric_line = tk.Menu(self.master, tearoff=0)
        self.parametric_line.add_command(label="Форма Эрмита", command=lambda: self.set_algorithm("hermite shape"))
        self.parametric_line.add_command(label="Форма Безье", command=lambda: self.set_algorithm("bezier shape"))
        self.parametric_line.add_command(label="B-сплайн", command=lambda: self.set_algorithm("b-spline"))

        self.menu_bar = tk.Menu(self.master)
        self.menu_bar.add_cascade(label="Отрезок", menu=self.line_menu)
        self.menu_bar.add_cascade(label="Линии второго порядка", menu=self.second_order_line_menu)
        self.menu_bar.add_cascade(label="Параметрические кривые", menu=self.parametric_line)

        self.master.config(menu=self.menu_bar)

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
