import gtk


class Struct:
    pass


class Image(object):
    "Fits image in the component"

    def __init__(self, pixbuf, on_resize = None):
        self.pixbuf     = pixbuf
        self.scale      = 1.0
        self.dx         = 0
        self.dy         = 0
        self.img_scaled     = None
        self.img_darkened   = None
        self.on_resize  = on_resize

        self.__setup()


    def get_root(self):
        return self.gui.evb


    def get_scale(self):
        return self.scale


    def get_image_size(self):
        return (self.img_scaled.get_width(), self.img_scaled.get_height())


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
        self.img_scaled   = self.pixbuf.scale_simple(width, height, gtk.gdk.INTERP_NEAREST)

        colorspace      = self.img_scaled.get_colorspace()
        has_alpha       = self.img_scaled.get_has_alpha()
        bits_per_sample = self.img_scaled.get_bits_per_sample()
        self.img_darkened = gtk.gdk.Pixbuf(colorspace, has_alpha, bits_per_sample, width, height)
        self.img_darkened.fill(0x00000000);
        self.img_scaled.composite(self.img_darkened, 0, 0, width, height, 0, 0, 1.0, 1.0, gtk.gdk.INTERP_HYPER, int(0.5*255));

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
        if self.img_scaled:
            item  = self.gui.image
            style = item.get_style()
            gc    = style.fg_gc[gtk.STATE_NORMAL]
            self.custom_draw(item.window, style, gc)


    def custom_draw(self, window, style, gc):
        window.draw_pixbuf(gc, self.img_scaled, 0, 0, self.dx, self.dy, -1, -1)
