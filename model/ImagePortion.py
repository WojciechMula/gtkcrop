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
        self.x = Number(0)
        self.y = Number(0)
        self.w = Number(maxwidth)
        self.h = Number(maxheight)

        self.maxwidth       = maxwidth
        self.maxheight      = maxheight
        self.aspectratio    = aspectratio


    def listen(self, handler):
        for component in (self.x, self.y, self.w, self.h):
            component.listen(handler)


    def get_rectangle(self):
        return (
            self.x.get(),
            self.y.get(),
            self.w.get(),
            self.h.get()
        )


    def get_dimensions(self):
        return (
            self.w.get(),
            self.h.get()
        )


    def get_coords(self):
        x, y, w, h = self.get_rectangle()

        return (x, y, x + w, y + h)

    def __str__(self):
        return "(%d, %d) - (%d, %d)" % self.get_coords()

