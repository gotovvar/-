class LineSecondOrderAlgorithm:

    @staticmethod
    def get_points_circle(x, y, *radius):
        dx = abs(x - radius[0])
        dy = abs(y - radius[1])
        radius = int((dx ** 2 + dy ** 2) ** 0.5)

        disp_x = x
        disp_y = y
        x = 0
        y = radius
        delta = (2 - 2 * radius)
        color = 'black'
        points = []
        while y >= 0:
            points.append((disp_x + x, disp_y + y, color))
            points.append((disp_x + x, disp_y - y, color))
            points.append((disp_x - x, disp_y + y, color))
            points.append((disp_x - x, disp_y - y, color))

            error = 2 * (delta + y) - 1
            if (delta < 0) and (error <= 0):
                x += 1
                delta = delta + (2 * x + 1)
                continue
            error = 2 * (delta - x) - 1
            if (delta > 0) and (error > 0):
                y -= 1
                delta = delta + (1 - 2 * y)
                continue
            x += 1
            y -= 1
            delta = delta + (2 * (x - y + 1))

        return points

    @staticmethod
    def get_points_ellipse(x1, y1, x2, y2):
        a = abs(x2 - x1) / 2
        b = abs(y2 - y1) / 2
        _x = 0
        _y = b
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        a_sqr = a * a
        b_sqr = b * b
        delta = 4 * b_sqr * ((_x + 1) * (_x + 1)) + a_sqr * ((2 * _y - 1) * (2 * _y - 1)) - 4 * a_sqr * b_sqr
        color = 'black'
        points = []

        while a_sqr * (2 * _y) > 2 * b_sqr * _x:
            points.append((center_x + _x, center_y + _y, color))
            points.append((center_x + _x, center_y - _y, color))
            points.append((center_x - _x, center_y + _y, color))
            points.append((center_x - _x, center_y - _y, color))
            if delta < 0:
                _x += 1
                delta += 4 * b_sqr * (2 * _x + 3)
            else:
                _x += 1
                delta = delta - 8 * a_sqr * (_y - 1) + 4 * b_sqr * (2 * _x + 3)
                _y -= 1
        delta = b_sqr * ((2 * _x + 1) * (2 * _x + 1)) + 4 * a_sqr * ((_y + 1) * (_y + 1)) - 4 * a_sqr * b_sqr
        while _y / 2 >= 0:
            points.append((center_x + _x, center_y + _y, color))
            points.append((center_x + _x, center_y - _y, color))
            points.append((center_x - _x, center_y + _y, color))
            points.append((center_x - _x, center_y - _y, color))
            if delta < 0:
                _y -= 1
                delta += 4 * a_sqr * (2 * _y + 3)
            else:
                _y -= 1
                delta = delta - 8 * b_sqr * (_x + 1) + 4 * a_sqr * (2 * _y + 3)
                _x += 1

        return points

    @staticmethod
    def get_points_parabola(x, y, end_x, end_y):
        center_x, center_y = x, y
        color = 'black'
        points = []
        a = abs(end_x - x)

        sy = 1 if y < end_y else -1

        for x in range(-a, a + 1):
            y = int(x * x // (2 * a) * sy)
            points.append((center_x + x, center_y + y, color))
            points.append((center_x - x, center_y + y, color))

        return points

    @staticmethod
    def get_points_hyperbole(x, y, end_x, end_y):
        center_x, center_y = x, y
        color = 'black'
        points = []
        a = abs(end_x - x)
        b = abs(end_y - y)

        for x in range(-a, a + 1):
            y = int(b * (1 + (x**2) / (a**2))**0.5)
            points.append((center_x + x, center_y + y, color))
            points.append((center_x - x, center_y + y, color))
            points.append((center_x + x, center_y - y, color))
            points.append((center_x - x, center_y - y, color))

        return points

