import math

def get_distance(points):
    (x1, y1), (x2, y2) = points
    return math.hypot(x2 - x1, y2 - y1)

def get_angle(p1, p2, p3):
    try:
        a = math.dist(p2, p3)
        b = math.dist(p1, p3)
        c = math.dist(p1, p2)
        if b * c == 0:
            return 0
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
        return math.degrees(angle)
    except:
        return 0
