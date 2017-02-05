OUTSIDE         = 'outside'
INSIDE          = 'inside'
LEFT            = 'left'
RIGHT           = 'right'
TOP             = 'top'
BOTTOM          = 'bottom'
LEFT_TOP        = 'lt'
RIGHT_TOP       = 'rt'
LEFT_BOTTOM     = 'lb'
RIGHT_BOTTOM    = 'rb'


class SelectionView(object):

    def __init__(self):
        self.set(0, 0, 0, 0)
        self.margin = 20


    def set(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


    def classify(self, x, y):

        def classify_1d(x, x0, x1, margin):
            if x < x0 or x > x1:
                return OUTSIDE

            if x <= x0 + margin:
                return LEFT

            if x >= x1 - margin:
                return RIGHT

            return INSIDE

        classify_x = classify_1d
        def classify_y(y, y0, height, margin):
            c = classify_1d(y, y0, height, margin)
            if c == LEFT:
                return TOP
            if c == RIGHT:
                return BOTTOM
            
            return c

        cx = classify_x(x, self.x0, self.x1, self.margin)
        cy = classify_y(y, self.y0, self.y1, self.margin)

        if cx == OUTSIDE or cy == OUTSIDE:
            return OUTSIDE

        if cx == INSIDE and cy == INSIDE:
            return INSIDE

        if cx == LEFT:
            if cy == TOP:
                return LEFT_TOP

            if cy == BOTTOM:
                return LEFT_BOTTOM

            assert cy == INSIDE
            return LEFT

        if cx == RIGHT:
            if cy == TOP:
                return RIGHT_TOP

            if cy == BOTTOM:
                return RIGHT_BOTTOM

            assert cy == INSIDE
            return RIGHT

        assert cx == INSIDE
        return cy

