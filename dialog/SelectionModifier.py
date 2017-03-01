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

        self.selection.set_pos_x0(self.x0 + dx)
        self.selection.set_pos_y0(self.y0 + dy)


class SelectionTop(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_y0(y)


class SelectionBottom(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_y1(y)


class SelectionLeft(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_x0(x)


class SelectionRight(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_x1(x)


class SelectionLeftTop(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_x0_y0(x, y)


class SelectionLeftBottom(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_x0_y1(x, y)


class SelectionRightTop(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_x1_y0(x, y)


class SelectionRightBottom(SelectionModifier):
    
    def do_update(self, x, y):
        self.selection.set_x1_y1(x, y)

