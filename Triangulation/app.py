import tkinter as tk
from scipy.spatial import Delaunay, Voronoi
import numpy as np


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.points = []

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_mouse_click)

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

    def handle_mouse_click(self, event):
        self.points.append((event.x, event.y))
        self.update_visualization()

    def update_visualization(self):
        self.canvas.delete("all")

        for point in self.points:
            x, y = point
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

        if len(self.points) > 2:
            points_array = np.array(self.points)
            delaunay = Delaunay(points_array)
            voronoi = Voronoi(points_array)

            for simplex in delaunay.simplices:
                vertices = [self.points[i] for i in simplex]
                vertices.append(vertices[0])
                coords = [coord for vertex in vertices for coord in vertex]
                self.canvas.create_line(coords, fill="red")

            for point_index, region in enumerate(voronoi.regions):
                if region and -1 not in region:
                    region_vertices = [voronoi.vertices[i] for i in region]
                    if point_index in voronoi.point_region:
                        coords = [coord for vertex in region_vertices for coord in vertex]
                        self.canvas.create_polygon(coords, outline="blue", fill="", width=1)

    def clear_canvas(self):
        self.points = []
        self.canvas.delete("all")
