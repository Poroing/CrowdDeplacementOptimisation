from pymunk.vec2d import Vec2d

class Segment(object):

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

def centrerPoint(point, centre):
    return point - centre

def avoirPositionProjection(vecteur1, vecteur2):
    return vecteur1.dot(vecteur2) / vecteur2.get_length_sqrd()

def avoirProjectionSurSegment(point, segment):
    point_centre = centrerPoint(point, segment.point2)
    direction_segment_centre = centrerPoint(segment.point1, segment.point2)
    t = avoirPositionProjection(point_centre, direction_segment_centre)
    if t < 0 or t > 1:
        return None
    return direction_segment_centre * t + segment.point2
