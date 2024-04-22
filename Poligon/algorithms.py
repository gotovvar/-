import math


def sorty_graham(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    start_point = min(points, key=lambda point: (point[1], point[0]))
    points.sort(key=lambda point: (math.atan2(point[1] - start_point[1], point[0] - start_point[0]), (point[0] - start_point[0])**2 + (point[1] - start_point[1])**2))
    stack = [start_point, points[0], points[1]]

    for i in range(2, len(points)):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], points[i]) != -1:
            stack.pop()
        stack.append(points[i])

    return stack


def sorty_jarvis(points):
    hull = [min(points, key=lambda p: p[1])]
    while True:
        endpoint = points[0]
        for point in points[1:]:
            if point == hull[-1]:
                continue
            turn = orientation(hull[-1], endpoint, point)
            if turn == 1 or (turn == 0 and distance(hull[-1], point) > distance(hull[-1], endpoint)):
                endpoint = point
        if endpoint == hull[0]:
            break
        hull.append(endpoint)

    return hull


def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def distance(p, q):
    return (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
