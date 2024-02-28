import tkinter as tk
from ToolPanel import ToolPanel
from algorithms.Line import LineAlgorithm
from algorithms.LineSecondOrder import LineSecondOrderAlgorithm


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

        self.tool_panel = ToolPanel(self.master)

        self.debug_mode = False
        self.debug_button = tk.Button(self.master, text="Debug Mode", command=self.toggle_debug)
        self.debug_button.pack(side=tk.LEFT)
        self.drawn_grid = False

        self.continue_button = tk.Button(self.master, text="Продолжить", command=self.continue_debug)

        self.clear_button = tk.Button(self.master, text="Очистить полотно", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT)

        self.debug_label = tk.Label(self.master, text="")
        self.debug_label.pack()

        self.debug_points = []

    def continue_debug(self):
        if self.debug_points:
            self.draw_line(self.debug_points)

    def set_algorithm(self, algorithm):
        self.tool_panel.set_algorithm(algorithm)

    def on_first_click(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        self.first_click_coords = (x, y)
        self.canvas.bind("<Button-1>", self.on_second_click)

    def on_second_click(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if self.tool_panel.algorithm == "dda":
            points = LineAlgorithm.get_points_line_dda(self.first_click_coords[0], self.first_click_coords[1], x, y)
        elif self.tool_panel.algorithm == "bresenham":
            points = LineAlgorithm.get_points_line_bresenham(self.first_click_coords[0], self.first_click_coords[1], x, y)
        elif self.tool_panel.algorithm == "wu":
            points = LineAlgorithm.get_points_line_wu(self.first_click_coords[0], self.first_click_coords[1], x, y)
        elif self.tool_panel.algorithm == "circle":
            points = LineSecondOrderAlgorithm.get_points_circle(self.first_click_coords[0], self.first_click_coords[1], x, y)
        elif self.tool_panel.algorithm == "ellipse":
            points = LineSecondOrderAlgorithm.get_points_ellipse(self.first_click_coords[0], self.first_click_coords[1], x, y)
        elif self.tool_panel.algorithm == "parabola":
            points = LineSecondOrderAlgorithm.get_points_parabola(self.first_click_coords[0], self.first_click_coords[1], x, y)
        else:
            points = LineSecondOrderAlgorithm.get_points_hyperbole(self.first_click_coords[0], self.first_click_coords[1], x, y)
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
