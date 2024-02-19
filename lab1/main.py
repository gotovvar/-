import tkinter as tk
from collections import deque


class GraphicsEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Graphics Editor")

        self.pixel_size = 10
        self.num_pixels_horizontal = 50
        self.num_pixels_vertical = 50

        self.canvas_width = self.num_pixels_horizontal * self.pixel_size
        self.canvas_height = self.num_pixels_vertical * self.pixel_size

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_first_click)
        self.first_click_coords = None

        self.menu_bar = tk.Menu(self.master)

        self.line_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.line_menu.add_command(label="ЦДА", command=lambda: self.set_algorithm("dda"))
        self.line_menu.add_command(label="Брезенхем", command=lambda: self.set_algorithm("bresenham"))
        self.line_menu.add_command(label="Ву", command=lambda: self.set_algorithm("wu"))
        self.menu_bar.add_cascade(label="Отрезок", menu=self.line_menu)

        self.second_order_line_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.second_order_line_menu.add_command(label="Окружность", command=lambda: self.set_algorithm("circle"))
        self.second_order_line_menu.add_command(label="Эллипс", command=lambda: self.set_algorithm("ellipse"))
        self.second_order_line_menu.add_command(label="Гипербола", command=lambda: self.set_algorithm("hyperbola"))
        self.second_order_line_menu.add_command(label="Парабола", command=lambda: self.set_algorithm("parabola"))
        self.menu_bar.add_cascade(label="Линии второго порядка", menu=self.second_order_line_menu)

        self.master.config(menu=self.menu_bar)

        self.debug_mode = False
        self.debug_button = tk.Button(self.master, text="Debug Mode", command=self.toggle_debug)
        self.debug_button.pack(side=tk.LEFT)
        self.continue_button = tk.Button(self.master, text="Продолжить", command=self.continue_debug)
        self.continue_button.pack(side=tk.LEFT)
        self.debug_pixels = deque()
        self.drawn_grid = False

        self.clear_button = tk.Button(self.master, text="Очистить полотно", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT)

        self.debug_label = tk.Label(self.master, text="")
        self.debug_label.pack()
        self.algorithm = "dda"

    def draw_debug_pixel(self):
        if self.debug_pixels:
            x, y = self.debug_pixels.popleft()
            self.canvas.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                         (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                         fill='black')
            self.master.after(1000, self.draw_debug_pixel)

    def continue_debug(self):
        self.draw_debug_pixel()

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def on_first_click(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        self.first_click_coords = (x, y)
        self.canvas.bind("<Button-1>", self.on_second_click)

    def on_second_click(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if self.algorithm == "dda":
            self.draw_line_dda(self.first_click_coords[0], self.first_click_coords[1], x, y)
        elif self.algorithm == "bresenham":
            self.draw_line_bresenham(self.first_click_coords[0], self.first_click_coords[1], x, y)
        elif self.algorithm == "wu":
            self.draw_line_wu(self.first_click_coords[0], self.first_click_coords[1], x, y)
            self.draw_line_bresenham(self.first_click_coords[0], self.first_click_coords[1], x, y)
        self.canvas.bind("<Button-1>", self.on_first_click)

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.debug_label.config(text="Debug Mode: ON")
            if not self.drawn_grid:
                self.draw_debug_grid()
        else:
            self.debug_label.config(text="Debug Mode: OFF")
            if not self.drawn_grid:
                self.canvas.delete("grid")

    def draw_debug_grid(self):
        for x in range(0, self.canvas_width, self.pixel_size):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="gray", tags="grid")
        for y in range(0, self.canvas_height, self.pixel_size):
            self.canvas.create_line(0, y, self.canvas_width, y, fill="gray", tags="grid")

    def draw_line_dda(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps

        for i in range(steps + 1):
            x = round(x1 + i * x_increment)
            y = round(y1 + i * y_increment)
            self.canvas.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                          (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                          fill='black')

        print("Line drawn using DDA algorithm.")

    def draw_line_bresenham(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        self.canvas.create_rectangle(x2 * self.pixel_size, y2 * self.pixel_size,
                                     (x2 + 1) * self.pixel_size, (y2 + 1) * self.pixel_size,
                                     fill="black")

        while x1 != x2 or y1 != y2:
            self.canvas.create_rectangle(x1 * self.pixel_size, y1 * self.pixel_size,
                                         (x1 + 1) * self.pixel_size, (y1 + 1) * self.pixel_size,
                                         fill="black")

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        print("Line drawn using Bresenham algorithm.")

    def draw_line_wu(self, x1, y1, x2, y2):
        def plot(x, y, c):
            color = int((1 - c) * 255)
            color_hex = '#{:02x}{:02x}{:02x}'.format(color, color, color)
            self.canvas.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                         (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                         fill=color_hex, outline="")

        def ipart(x):
            return int(x)

        def fpart(x):
            return x - int(x)

        def rfpart(x):
            return 1 - fpart(x)

        steep = abs(y2 - y1) > abs(x2 - x1)
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1
        gradient = dy / dx if dx != 0 else 1

        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = rfpart(x1 + 0.5)
        xpxl1 = xend
        ypxl1 = ipart(yend)

        if steep:
            plot(ypxl1, xpxl1, rfpart(yend) * xgap)
            plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap)
        else:
            plot(xpxl1, ypxl1, rfpart(yend) * xgap)
            plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)
        intery = yend + gradient

        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xgap = fpart(x2 + 0.5)
        xpxl2 = xend
        ypxl2 = ipart(yend)
        if steep:
            plot(ypxl2, xpxl2, rfpart(yend) * xgap)
            plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap)
        else:
            plot(xpxl2, ypxl2, rfpart(yend) * xgap)
            plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

        if steep:
            for x in range(xpxl1 + 1, xpxl2):
                plot(ipart(intery), x, rfpart(intery))
                plot(ipart(intery) + 1, x, fpart(intery))
                intery += gradient
        else:
            for x in range(xpxl1 + 1, xpxl2):
                plot(x, ipart(intery), rfpart(intery))
                plot(x, ipart(intery) + 1, fpart(intery))
                intery += gradient

        print("Line drawn using Wu algorithm.")

    def clear_canvas(self):
        if not self.debug_mode:
            self.canvas.delete("all")
        else:
            self.canvas.delete("all")
            if not self.drawn_grid:
                self.draw_debug_grid()


def main():
    root = tk.Tk()
    app = GraphicsEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
