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

        self.maxwidth           = maxwidth
        self.maxheight          = maxheight
        self.aspectratio        = aspectratio
        self.use_aspectratio    = (aspectratio != None)


    def select_all(self):
        self.__set_coords(0, 0, self.maxwidth, self.maxheight)


    def set_rectangle_unsafe(self, x, y, width, height):
        if x < 0:
            raise ValueError("x must not be less than zero")

        if x > self.maxwidth:
            raise ValueError("x must not be greater than %d" % self.maxwidth)

        if y < 0:
            raise ValueError("y must not be less than zero")

        if y > self.maxheight:
            raise ValueError("y must not be greater than %d" % self.maxheight)

        if width < 0:
            raise ValueError("width must not be less than zero")

        if x + width > self.maxwidth:
            raise ValueError("width must not be greater than %d" % (self.maxwidth - x))

        if height < 0:
            raise ValueError("height must not be less than zero")

        if x + height > self.maxheight:
            raise ValueError("height must not be greater than %d" % (self.maxheight - x))

        self.__set_coords(x, y, x+width, y+height)


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

        x0, y0, x1, y1 = self.get_coords()

        y = max(y, 0)
        y = min(y, y1)

        if self.use_aspectratio == False:
            self.y0.set(y)

        else:
            y0 = y
            x  = (x0 + x1) / 2
            w  = int((y1 - y0) * self.aspectratio)
            w2 = w / 2

            x0 = x - w2
            x1 = x + (w - w2)

            self.__set_coords(x0, y0, x1, y1)


    def set_y1(self, y):

        x0, y0, x1, y1 = self.get_coords()

        y = max(y, y0)
        y = min(y, self.maxheight)

        if self.use_aspectratio == False:
            self.y1.set(y)

        else:
            y1 = y
            x  = (x0 + x1) / 2
            w  = int((y1 - y0) * self.aspectratio)
            w2 = w/2

            x0 = x - w2
            x1 = x + (w - w2)

            self.__set_coords(x0, y0, x1, y1)


    def set_x0(self, x):

        x0, y0, x1, y1 = self.get_coords()

        x = max(x, 0)
        x = min(x, x1)

        if self.use_aspectratio == False:
            self.x0.set(x)

        else:
            x0 = x
            y  = (y0 + y1)/2
            h  = int((x1 - x) / self.aspectratio)
            h2 = h/2

            y0 = y - h2
            y1 = y + (h - h2)

            self.__set_coords(x0, y0, x1, y1)


    def set_x1(self, x):

        x0, y0, x1, y1 = self.get_coords()

        x = max(x, x0)
        x = min(x, self.maxwidth)

        if self.use_aspectratio == False:
            self.x1.set(x)

        else:
            x1 = x
            y  = (y0 + y1)/2
            h  = int((x - x0) / self.aspectratio)
            h2 = h/2

            y0 = y - h2
            y1 = y + (h - h2)

            self.__set_coords(x0, y0, x1, y1)


    def __set_coords(self, x0, y0, x1, y1):
        if x0 < 0 or x0 > x1 or x1 > self.maxwidth:
            return

        if y0 < 0 or y0 > y1 or y1 > self.maxheight:
            return

        self.x0.set(x0)
        self.x1.set(x1)
        self.y0.set(y0)
        self.y1.set(y1)
        return True


    def set_x0_y0(self, x, y):

        if self.use_aspectratio == False:
            self.set_x0(x)
            self.set_y0(y)
        else:
            x0, y0, x1, y1 = self.get_coords()

            x0 = x
            y0 = y
            w = x1 - x0
            h = y1 - y0

            if self.aspectratio >= 1.0:
                h  = int(w / self.aspectratio)
                y0 = y1 - h
            else:
                w  = int(h * self.aspectratio)
                x0 = x1 - w

            self.__set_coords(x0, y0, x1, y1)


    def set_x0_y1(self, x, y):

        if self.use_aspectratio == False:
            self.set_x0(x)
            self.set_y1(y)
        else:
            x0, y0, x1, y1 = self.get_coords()

            x0 = x
            y1 = y
            w = x1 - x0
            h = y1 - y0

            if self.aspectratio >= 1.0:
                h  = int(w / self.aspectratio)
                y1 = y0 + h
            else:
                w  = int(h * self.aspectratio)
                x0 = x1 - w

            self.__set_coords(x0, y0, x1, y1)


    def set_x1_y0(self, x, y):

        if self.use_aspectratio == False:
            self.set_x1(x)
            self.set_y0(y)
        else:
            x0, y0, x1, y1 = self.get_coords()

            x1 = x
            y0 = y
            w = x1 - x0
            h = y1 - y0

            if self.aspectratio > 1.0:
                h  = int(w / self.aspectratio)
                y0 = y1 - h
            else:
                w  = int(h * self.aspectratio)
                x1 = x0 + w

            self.__set_coords(x0, y0, x1, y1)


    def set_x1_y1(self, x, y):

        if self.use_aspectratio == False:
            self.set_x1(x)
            self.set_y1(y)
        else:
            x0, y0, x1, y1 = self.get_coords()

            x1 = x
            y1 = y
            w = x1 - x0
            h = y1 - y0

            if self.aspectratio > 1.0:
                h  = int(w / self.aspectratio)
                y1 = y0 + h
            else:
                w  = int(h * self.aspectratio)
                x1 = x0 + w

            self.__set_coords(x0, y0, x1, y1)


    def set_width(self, w):
        self.set_x1(self.x0.get() + w)


    def set_height(self, h):
        self.set_y1(self.y0.get() + h)


    def use_fixed_aspectratio(self, flag):
        self.use_aspectratio = flag
        self.__force_aspect_ratio()

    def set_aspect(self, aspectratio):
        self.aspectratio = aspectratio
        self.__force_aspect_ratio()


    def __force_aspect_ratio(self):
        if not self.use_aspectratio:
            return

        x0, y0, x1, y1 = self.get_coords()

        w = x1 - x0
        h = y1 - y0

        while True:

            if self.aspectratio > 1.0:
                h  = int(w / self.aspectratio)
                y1 = y0 + h
            else:
                w  = int(h * self.aspectratio)
                x1 = x0 + w

            if self.__set_coords(x0, y0, x1, y1):
                break
            else:
                if self.aspectratio > 1.0:
                    h /= 2
                    if h == 0:
                        break
                else:
                    w /= 2
                    if w == 0:
                        break


    def listen(self, handler):
        for component in (self.x0, self.y0, self.x1, self.y1):
            component.listen(handler)


    def notify(self):
        self.x0.notify()


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

