import numpy as np
import tkinter as tk


class Shape:
    def __init__(self):
        self.points = []

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.points = [tuple(map(float, line.strip().split())) for line in file]
            if len(self.points) < 3:
                raise ValueError("Необходимо загрузить как минимум 3 точки для создания фигуры.")

    def move(self, direction, axis):
        for i, point in enumerate(self.points):
            new_point = list(point)
            if axis == 'x':
                new_point[0] += direction * 0.2
            elif axis == 'y':
                new_point[1] += direction * 0.2
            elif axis == 'z':
                new_point[2] += direction * 0.2
            self.points[i] = tuple(round(coord, 1) for coord in new_point)

    def rotate(self, rotation_matrix):
        for i, point in enumerate(self.points):
            new_point = np.dot(rotation_matrix, point)
            self.points[i] = tuple(round(coord, 1) for coord in new_point)

    def scale(self, scale_factor):
        center = np.mean(self.points, axis=0)
        self.points = [(point[0] - center[0], point[1] - center[1], point[2] - center[2]) for point in self.points]
        self.points = [(point[0] * scale_factor, point[1] * scale_factor, point[2] * scale_factor) for point in self.points]
        self.points = [(point[0] + center[0], point[1] + center[1], point[2] + center[2]) for point in self.points]

    def show_points(self, points_frame):
        self.clear_points(points_frame)
        for i, point in enumerate(self.points):
            rounded_point = tuple(round(coord, 1) for coord in point)
            point_label = tk.Label(points_frame, text=f"Точка {i+1}: {rounded_point}")
            point_label.pack(anchor=tk.W)

    @staticmethod
    def clear_points(points_frame):
        for widget in points_frame.winfo_children():
            widget.destroy()
