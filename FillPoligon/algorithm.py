class Algorithm:
    def __init__(self, root):
        self.root = root

    def fill_polygon_with_order_line(self):
        self.root.canvas.delete("fill")
        bbox = self.root.canvas.bbox(self.root.tag_id)
        if bbox:
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = bbox
            for y in range(int(top_left_y), int(bottom_right_y)):
                intersections = []
                for x in range(int(top_left_x), int(bottom_right_x)):
                    if self.is_inside_polygon(x, y):
                        intersections.append(x)
                for i in range(0, len(intersections), 2):
                    if i + 1 < len(intersections):
                        x1, x2 = intersections[i], intersections[i + 1]
                        self.root.canvas.create_rectangle(x1, y, x2, y, fill='black', tags="fill")
                        self.root.update()

    def fill_polygon_with_active_edges(self):
        self.root.canvas.delete("fill")
        fill_coords = []
        active_edges = self.get_active_edges()
        if active_edges:
            for y, edges in active_edges.items():
                for i in range(0, len(edges) - 1, 2):
                    x1, x2 = edges[i], edges[i + 1]
                    fill_coords.extend([x1, y, x2, y])
                    self.root.canvas.create_rectangle(x1, y, x2, y, fill='black', tags="fill")
                    self.root.update()

    def get_active_edges(self):
        active_edges = {}
        bbox = self.root.canvas.bbox(self.root.tag_id)
        if bbox:
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = bbox
            for y in range(int(top_left_y), int(bottom_right_y)):
                intersections = []
                for x in range(int(top_left_x), int(bottom_right_x)):
                    if self.is_inside_polygon(x, y):
                        intersections.append(x)
                if intersections:
                    active_edges[y] = intersections
        return active_edges

    def fill_polygon_with_seed(self):
        self.root.canvas.delete("fill")
        polygon_coords = self.root.canvas.coords(self.root.tag_id)
        seed_x, seed_y = polygon_coords[:2]
        self.fill_with_seed(seed_x, seed_y)

    def fill_with_seed(self, x, y):
        filled_pixels = set()
        stack = [(int(x), int(y))]

        while stack:
            current_x, current_y = stack.pop()
            if 0 <= current_x < self.root.canvas.winfo_width() and 0 <= current_y < self.root.canvas.winfo_height():
                if (current_x, current_y) not in filled_pixels:
                    if self.is_inside_polygon(current_x, current_y):
                        self.root.canvas.create_rectangle(current_x, current_y, current_x, current_y, fill='black', tags="fill")
                        filled_pixels.add((current_x, current_y))
                        self.root.update()
                        stack.append((current_x + 1, current_y))
                        stack.append((current_x - 1, current_y))
                        stack.append((current_x, current_y + 1))
                        stack.append((current_x, current_y - 1))

    def fill_polygon_with_seed_line(self):
        self.root.canvas.delete("fill")
        polygon_coords = self.root.canvas.coords(self.root.tag_id)
        seed_x, seed_y = polygon_coords[:2]
        self.fill_with_seed_line(seed_x, seed_y)

    def fill_with_seed_line(self, x, y):
        filled_pixels = set()
        stack = [(int(x), int(y))]

        while stack:
            current_x, current_y = stack.pop()
            if 0 <= current_x < self.root.canvas.winfo_width() and 0 <= current_y < self.root.canvas.winfo_height():
                if (current_x, current_y) not in filled_pixels:
                    if self.is_inside_polygon(current_x, current_y):
                        x_left = current_x
                        x_right = current_x
                        while x_left >= 0 and self.is_inside_polygon(x_left, current_y):
                            filled_pixels.add((x_left, current_y))
                            self.root.canvas.create_rectangle(x_left, current_y, x_left, current_y, fill='black', tags="fill")
                            self.root.update()
                            x_left -= 1
                        while x_right < self.root.canvas.winfo_width() and self.is_inside_polygon(x_right, current_y):
                            filled_pixels.add((x_right, current_y))
                            self.root.canvas.create_rectangle(x_right, current_y, x_right, current_y, fill='black', tags="fill")
                            self.root.update()
                            x_right += 1
                        for new_y in [current_y + 1, current_y - 1]:
                            for new_x in range(x_left + 1, x_right):
                                stack.append((new_x, new_y))

    def is_inside_polygon(self, x, y):
        return self.root.canvas.find_overlapping(x, y, x, y)

    def create_fill_line(self, x1, y1, x2, y2):
        self.root.canvas.create_line(x1, y1, x2, y2, tags="fill")
