class LineAlgorithm:

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
