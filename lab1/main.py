from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random


class GraphicsEditor:
    def __init__(self, master):
        self.master = master

        self.toolbar = Frame(self.master)
        self.toolbar.pack(side=TOP, pady=10)

        self.clear_button = Button(self.toolbar, text="Очистить", command=self.clear_canvas)
        self.clear_button.pack(side=LEFT, padx=5)

        self.segment_button = Button(self.toolbar, text="Отрезок", command=self.show_algorithms)
        self.segment_button.pack(side=LEFT, padx=5)

        self.canvas = Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw)

        self.algorithm_frame = Frame(self.master)

        self.algorithm_cda_button = Button(self.algorithm_frame, text="Алг. ЦДА", command=self.algorithm_cda)
        self.algorithm_cda_button.pack(side=LEFT, padx=5)

        self.algorithm_brezenhem_button = Button(self.algorithm_frame, text="Алг. Брезенхема",
                                                 command=self.algorithm_brezenhem)
        self.algorithm_brezenhem_button.pack(side=LEFT, padx=5)

        self.algorithm_by_button = Button(self.algorithm_frame, text="Алг. By", command=self.algorithm_by)
        self.algorithm_by_button.pack(side=LEFT, padx=5)

        self.cancel_button = Button(self.algorithm_frame, text="Отмена", command=self.cancel)
        self.cancel_button.pack(side=LEFT, padx=5)

    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")

    def clear_canvas(self):
        self.canvas.delete("all")

    def show_algorithms(self):
        self.clear_button.pack_forget()
        self.segment_button.pack_forget()

        self.algorithm_frame.pack(side=TOP, pady=10)

    def algorithm_cda(self):
        x1, y1 = random.randint(0, 10), random.randint(0, 10)
        x2, y2 = random.randint(0, 10), random.randint(0, 10)

        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps

        points = [(round(x1), round(y1))]
        i = 1
        while i <= steps:
            x1 += x_increment
            y1 += y_increment
            points.append((round(x1), round(y1)))
            i += 1

        self.pixel_image(points)

    def algorithm_brezenhem(self):
        x1, y1 = random.randint(0, 10), random.randint(0, 10)
        x2, y2 = random.randint(0, 10), random.randint(0, 10)

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        err = 2*dy - dx

        points = [(x1, y1)]
        i = 1
        while i <= dx:
            if err >= 0:
                y1 += sy
                err -= 2*dx
            x1 += sx
            err += 2*dy
            i += 1
            points.append((x1, y1))

        self.pixel_image(points)

    def algorithm_by(self):
        pass

    def pixel_image(self, points):

        squares = np.zeros((11, 11))
        for x, y in points:
            squares[y, x] = 1

        fig, ax = plt.subplots()
        ax.imshow(squares, cmap='binary', interpolation='nearest', origin='lower')

        ax.set_xticks(np.arange(0, 11, 1))
        ax.set_yticks(np.arange(0, 11, 1))
        ax.grid(color='black', linewidth=0.5)

        x_coords, y_coords = zip(*points)
        plt.plot(x_coords, y_coords, color='red', linestyle='-')

        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
        
    def cancel(self):
        self.algorithm_frame.pack_forget()
        self.clear_button.pack(side=LEFT, padx=5)
        self.segment_button.pack(side=LEFT, padx=5)


if __name__ == "__main__":
    root = Tk()
    app = GraphicsEditor(root)
    root.mainloop()
