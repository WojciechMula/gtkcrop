from Observer import Observer

class Number(Observer):
    def __init__(self, x):
        super(Number, self).__init__()
        self.__value = x


    def set(self, x):
        if x != self.__value:
            self.__value = x
            notify()

    def get(self):
        return self.__value


class ImagePortion:
    def __init__(self, maxwidth, maxheight):
        self.x = Number(0)
        self.y = Number(0)
        self.w = Number(maxwidth)
        self.h = Number(maxheight)

        self.maxwidth  = maxwidth
        self.maxheight = maxheight

