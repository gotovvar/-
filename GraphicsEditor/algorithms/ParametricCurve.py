class ParametricCurve:

    @staticmethod
    def get_points_b_spline_curve(points):
        spline_points = []
        color = 'black'

        for i in range(len(points) - 1):
            p0 = points[i]
            p1 = points[i + 1]

            t0 = (p1[0] - points[i - 1][0]) / 2 if i > 0 else 0
            t1 = (points[i + 2][0] - p0[0]) / 2 if i < len(points) - 2 else 0

            for t in range(101):
                t /= 100
                h1 = 2 * pow(t, 3) - 3 * pow(t, 2) + 1
                h2 = -2 * pow(t, 3) + 3 * pow(t, 2)
                h3 = pow(t, 3) - 2 * pow(t, 2) + t
                h4 = pow(t, 3) - pow(t, 2)

                x = h1 * p0[0] + h2 * p1[0] + h3 * t0 + h4 * t1
                y = h1 * p0[1] + h2 * p1[1] + h3 * t0 + h4 * t1

                spline_points.append((x, y, color))

        return spline_points

    @staticmethod
    def get_points_bezier_curve():
        pass

    @staticmethod
    def get_points_hermite_curve():
        pass
