class SelectionModifier(object):
    def __init__(self, selection, x, y):
        self.selection = selection
        self.x = x
        self.y = y
        self.x0, self.y0, self.x1, self.y1 = selection.get_coords() # take a snapshot

    def update(self, x, y):
        self.do_update(x, y)


class SelectionInside(SelectionModifier):

    def do_update(self, x, y):
        dx = x - self.x
        dy = y - self.y

        self.selection.x.set(self.x0 + dx)
        self.selection.y.set(self.y0 + dy)
