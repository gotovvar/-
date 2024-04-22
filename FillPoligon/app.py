import tkinter as tk
from algorithm import Algorithm


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Графический редактор")
        self.geometry("600x600")
        self.algorithm = Algorithm(self)

        self.canvas = tk.Canvas(self, width=500, height=500, bg='white')
        self.canvas.pack()

        self.fill_button = tk.Button(self, text="Ordered list of edges", command=self.algorithm.fill_polygon_with_order_line)
        self.fill_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.fill_active_edges_button = tk.Button(self, text="Active Edges", command=self.algorithm.fill_polygon_with_active_edges)
        self.fill_active_edges_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.fill_seed_button = tk.Button(self, text="Seed", command=self.algorithm.fill_polygon_with_seed)
        self.fill_seed_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.fill_seed_line_button = tk.Button(self, text="Seed Line", command=self.algorithm.fill_polygon_with_seed_line)
        self.fill_seed_line_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas.bind("<B1-Motion>", self.draw_line_with_event)

        polygon_coords = [x / 2 for x in [100, 90, 140, 200, 250, 300, 350, 300, 400, 200]]
        self.tag_id = self.canvas.create_polygon(polygon_coords, outline='black', fill="", tags='polygon')

        self.selected_algorithm = None
        self.is_drawing = False
        self.start_x, self.start_y = None, None

    def draw_line_with_event(self, event):
        if self.is_drawing:
            self.canvas.delete("line")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, tags="line")

    def end_drawing(self, event):
        if self.selected_algorithm:
            self.selected_algorithm(self.start_x, self.start_y, event.x, event.y)
