import gtk


class Struct:
    pass


class Image(object):
    "Fits image in the component"

    def __init__(self, pixbuf, on_resize = None):
        self.pixbuf     = pixbuf
        self.displayed  = None
        self.scale      = 1.0
        self.dx         = 0
        self.dy         = 0
        self.on_resize  = on_resize

        self.__setup()


    def get_root(self):
        return self.gui.evb


    def get_scale(self):
        return self.scale


    def __setup(self):
        self.gui = Struct()
        self.__create_gui()
        self.__connect()


    def __create_gui(self):
        self.gui.evb    = gtk.EventBox()
        self.gui.image  = gtk.DrawingArea()
        self.gui.evb.add(self.gui.image)


    def __connect(self):
        self.gui.evb.connect("size_allocate", self.__size_allocate__event)
        self.gui.image.connect("expose_event", self.__expose_event)


    def scale_pixbuf(self, width, height):
        W = self.pixbuf.get_width()
        H = self.pixbuf.get_height()

        try:
            fw = width/float(W)
            fh = height/float(H)
            self.scale = min(fw, fh, 1.0)
        except ZeroDivisionError:
            self.current = None
            return

        width  = int(self.scale * W)
        height = int(self.scale * H)
        self.displayed = self.pixbuf.scale_simple(width, height, gtk.gdk.INTERP_NEAREST)

        return (width, height)


    # handlers
    def __size_allocate__event(self, widget, rect):
        ret = self.scale_pixbuf(rect.width, rect.height)
        if ret:
            w, h = ret
            self.dx = (rect.width  - w)/2
            self.dy = (rect.height - h)/2

            if self.on_resize:
                self.on_resize()


    def __expose_event(self, widget, event):
        if self.displayed:
            item  = self.gui.image
            style = item.get_style()
            gc    = style.fg_gc[gtk.STATE_NORMAL]
            item.window.draw_pixbuf(gc, self.displayed, 0, 0, self.dx, self.dy, -1, -1)

        self.custom_draw(item.window, style, gc)


    def custom_draw(self, window, style, gc):
        pass
