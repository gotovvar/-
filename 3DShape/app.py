import tkinter as tk
from shape import Shape
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from help_window import HelpWindow


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("3D фигуры")
        self.geometry("1000x600")

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.points_frame = tk.Frame(self)
        self.points_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.shape = Shape()

        self.load_file_button = tk.Button(self.menu_frame, text="Загрузить из файла", command=self.load_from_file)
        self.load_file_button.pack(side=tk.TOP, pady=(10, 0), padx=10, anchor='center')

        self.help_button = tk.Button(self.menu_frame, text="Помощь", command=self.show_help_window)
        self.help_button.pack(side=tk.BOTTOM, pady=(0, 10), padx=10, anchor='center')

        self.bind("1", lambda event, direction=1: self.move_figure(event, direction, axis='x'))
        self.bind("2", lambda event, direction=-1: self.move_figure(event, direction, axis='x'))
        self.bind("3", lambda event, direction=1: self.move_figure(event, direction, axis='y'))
        self.bind("4", lambda event, direction=-1: self.move_figure(event, direction, axis='y'))
        self.bind("5", lambda event, direction=1: self.move_figure(event, direction, axis='z'))
        self.bind("6", lambda event, direction=-1: self.move_figure(event, direction, axis='z'))

        self.bind("7", self.rotate_x)
        self.bind("8", self.rotate_y)
        self.bind("9", self.rotate_z)

        self.bind("-", self.scale_down)
        self.bind("+", self.scale_up)

    def load_from_file(self, event=None):
        filename = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
        if filename:
            try:
                self.shape.load_from_file(filename)
                self.update_figure()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def update_figure(self):
        self.ax.cla()
        if self.shape.points:
            x, y, z = zip(*self.shape.points)
            self.ax.plot(x + (x[0],), y + (y[0],), z + (z[0],), c='b')
            self.ax.set_xlim(-3, 3)
            self.ax.set_ylim(-3, 3)
            self.ax.set_zlim(-3, 3)
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')
            self.canvas.draw()

            self.shape.show_points(self.points_frame)

    def move_figure(self, event, direction, axis):
        self.shape.move(direction, axis)
        self.update_figure()

    def rotate_x(self, event=None):
        rotation_matrix = np.array([[1, 0, 0], [0, np.cos(np.pi/6), -np.sin(np.pi/6)], [0, np.sin(np.pi/6), np.cos(np.pi/6)]])
        self.shape.rotate(rotation_matrix)
        self.update_figure()

    def rotate_y(self, event=None):
        rotation_matrix = np.array([[np.cos(np.pi/6), 0, np.sin(np.pi/6)], [0, 1, 0], [-np.sin(np.pi/6), 0, np.cos(np.pi/6)]])
        self.shape.rotate(rotation_matrix)
        self.update_figure()

    def rotate_z(self, event=None):
        rotation_matrix = np.array([[np.cos(np.pi/6), -np.sin(np.pi/6), 0], [np.sin(np.pi/6), np.cos(np.pi/6), 0], [0, 0, 1]])
        self.shape.rotate(rotation_matrix)
        self.update_figure()

    def scale_up(self, event):
        self.shape.scale(1.1)
        self.update_figure()

    def scale_down(self, event):
        self.shape.scale(0.9)
        self.update_figure()

    def show_help_window(self):
        help_window = HelpWindow(self)
        help_window.grab_set()

