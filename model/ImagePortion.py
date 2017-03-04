from Observer import Observer

class Number(Observer):
    def __init__(self, x):
        super(Number, self).__init__()
        self.__value = x


    def set(self, x):
        if x != self.__value:
            self.__value = x
            self.notify()
            return True
        else:
            return False

    def get(self):
        return self.__value


class ImagePortion:
    def __init__(self, maxwidth, maxheight, aspectratio = None):
        self.x0 = Number(0)
        self.y0 = Number(0)
        self.x1 = Number(maxwidth)
        self.y1 = Number(maxheight)

        self.maxwidth       = maxwidth
        self.maxheight      = maxheight
        self.aspectratio    = aspectratio


    def set_pos_x0(self, x):
        x0 = self.x0.get()
        x1 = self.x1.get()
        w  = x1 - x0

        x  = max(x, 0)
        x  = min(x, self.maxwidth - w)
            
        self.x0.set(x)
        self.x1.set(x + w)


    def set_pos_y0(self, y):
        y0 = self.y0.get()
        y1 = self.y1.get()
        h  = y1 - y0

        y  = max(y, 0)
        y  = min(y, self.maxheight - h)
            
        self.y0.set(y)
        self.y1.set(y + h)


    def set_y0(self, y):

        y0 = self.y0.get()
        y1 = self.y1.get()

        y = max(y, 0)
        y = min(y, y1)

        self.y0.set(y)


    def set_y1(self, y):

        y0 = self.y0.get()
        y1 = self.y1.get()

        y = max(y, y0)
        y = min(y, self.maxheight)

        self.y1.set(y)


    def set_x0(self, x):

        x0 = self.x0.get()
        x1 = self.x1.get()

        x = max(x, 0)
        x = min(x, x1)

        self.x0.set(x)


    def set_x1(self, x):

        x0 = self.x0.get()
        x1 = self.x1.get()

        x = max(x, x0)
        x = min(x, self.maxwidth)

        self.x1.set(x)


    def set_x0_y0(self, x, y):

        if self.aspectratio is None:
            self.set_x0(x)
            self.set_y0(y)
        else:
            raise NotImplemented


    def set_x0_y1(self, x, y):

        if self.aspectratio is None:
            self.set_x0(x)
            self.set_y1(y)
        else:
            raise NotImplemented


    def set_x1_y0(self, x, y):

        if self.aspectratio is None:
            self.set_x1(x)
            self.set_y0(y)
        else:
            raise NotImplemented


    def set_x1_y1(self, x, y):

        if self.aspectratio is None:
            self.set_x1(x)
            self.set_y1(y)
        else:
            raise NotImplemented


    def set_width(self, w):
        if self.aspectratio is None:
            self.set_x1(self.x0.get() + w)
        else:
            raise NotImplemented


    def set_height(self, h):
        if self.aspectratio is None:
            self.set_y1(self.y0.get() + h)
        else:
            raise NotImplemented


    def listen(self, handler):
        for component in (self.x0, self.y0, self.x1, self.y1):
            component.listen(handler)


    def get_rectangle(self):
        x0 = self.x0.get()
        y0 = self.y0.get()
        x1 = self.x1.get()
        y1 = self.y1.get()

        return (x0, y0, x1 - x0, y1 - y0)


    def get_dimensions(self):
        x0 = self.x0.get()
        y0 = self.y0.get()
        x1 = self.x1.get()
        y1 = self.y1.get()

        return (x1 - x0, y1 - y0)


    def get_coords(self):
        x0 = self.x0.get()
        y0 = self.y0.get()
        x1 = self.x1.get()
        y1 = self.y1.get()

        return (x0, y0, x1, y1)

    def __str__(self):
        return "(%d, %d) - (%d, %d)" % self.get_coords()

