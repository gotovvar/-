import tkinter as tk


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
        self.drawn_grid = False

        self.continue_button = tk.Button(self.master, text="Продолжить", command=self.continue_debug)

        self.clear_button = tk.Button(self.master, text="Очистить полотно", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT)

        self.debug_label = tk.Label(self.master, text="")
        self.debug_label.pack()
        self.algorithm = "dda"

        self.debug_points = []

    def continue_debug(self):
        if self.debug_points:
            self.draw_line(self.debug_points)

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def on_first_click(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        self.first_click_coords = (x, y)
        self.canvas.bind("<Button-1>", self.on_second_click)

    def on_second_click(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if self.algorithm == "dda":
            points = self.get_points_line_dda(self.first_click_coords[0], self.first_click_coords[1], x, y)
            self.draw_line(points)
        elif self.algorithm == "bresenham":
            points = self.get_points_line_bresenham(self.first_click_coords[0], self.first_click_coords[1], x, y)
            self.draw_line(points)
        elif self.algorithm == "wu":
            points = self.get_points_line_wu(self.first_click_coords[0], self.first_click_coords[1], x, y)
            self.draw_line(points)
        self.canvas.bind("<Button-1>", self.on_first_click)

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.debug_label.config(text="Debug Mode: ON")
            if not self.drawn_grid:
                self.draw_debug_grid()
            self.continue_button.pack(side=tk.TOP)
        else:
            self.debug_label.config(text="Debug Mode: OFF")
            if not self.drawn_grid:
                self.canvas.delete("grid")
            self.continue_button.pack_forget()

    def draw_debug_grid(self):
        for x in range(0, self.canvas_width, self.pixel_size):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="gray", tags="grid")
        for y in range(0, self.canvas_height, self.pixel_size):
            self.canvas.create_line(0, y, self.canvas_width, y, fill="gray", tags="grid")

    def draw_line(self, points):
        if self.debug_mode:
            self.debug_points = points
            x, y, color = self.debug_points.pop(0)
            self.canvas.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                         (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                         fill=color, outline="")
        else:
            for x, y, color in points:
                self.canvas.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                             (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                             fill=color, outline="")

    @staticmethod
    def get_points_line_dda(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps
        color = 'black'

        points = []
        for i in range(steps + 1):
            x = round(x1 + i * x_increment)
            y = round(y1 + i * y_increment)
            points.append((x, y, color))

        return points

    @staticmethod
    def get_points_line_bresenham(x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        color = 'black'

        points = []

        while x1 != x2 or y1 != y2:
            points.append((x1, y1, color))

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        points.append((x2, y2, color))
        return points

    @staticmethod
    def get_points_line_wu(x1, y1, x2, y2):
        def definition_shade(value):
            color = int((1 - value) * 255)
            color_hex = '#{:02x}{:02x}{:02x}'.format(color, color, color)
            return color_hex

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

        points = []

        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xpxl1 = xend
        ypxl1 = ipart(yend)

        if steep:
            points.append((ypxl1, xpxl1, definition_shade(rfpart(yend))))
            points.append((ypxl1 + 1, xpxl1, definition_shade(fpart(yend))))
        else:
            points.append((xpxl1, ypxl1, definition_shade(rfpart(yend))))
            points.append((xpxl1, ypxl1 + 1, definition_shade(fpart(yend))))

        intery = yend + gradient
        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xpxl2 = xend
        ypxl2 = ipart(yend)

        if steep:
            for x in range(xpxl1 + 1, xpxl2):
                points.append((ipart(intery), x, definition_shade(rfpart(intery))))
                points.append((ipart(intery) + 1, x, definition_shade(fpart(intery))))
                intery += gradient
        else:
            for x in range(xpxl1 + 1, xpxl2):
                points.append((x, ipart(intery), definition_shade(rfpart(intery))))
                points.append((x, ipart(intery) + 1, definition_shade(fpart(intery))))
                intery += gradient

        if steep:
            points.append((ypxl2, xpxl2, definition_shade(rfpart(yend))))
            points.append((ypxl2 + 1, xpxl2, definition_shade(fpart(yend))))
        else:
            points.append((xpxl2, ypxl2, definition_shade(rfpart(yend))))
            points.append((xpxl2, ypxl2 + 1, definition_shade(fpart(yend))))

        return points

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
