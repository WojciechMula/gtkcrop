import gtk


class Struct:
    pass


class SelectionInputWidget:

    def __init__(self, selection):
        self.selection = selection
        self.__setup()


    def get_root(self):
        return self.root


    def __setup(self):
        self.gui = Struct()
        self.__create_gui()
        self.__connect()


    def __create_gui(self):

        def create_label(text):
            label = gtk.Label()
            label.set_text(text)
            label.set_justify(gtk.JUSTIFY_RIGHT)
          
            return label


        self.gui.x0 = gtk.SpinButton()
        self.gui.y0 = gtk.SpinButton()
        self.gui.x1 = gtk.SpinButton()
        self.gui.y1 = gtk.SpinButton()
        self.gui.w  = gtk.SpinButton()
        self.gui.h  = gtk.SpinButton()

        for item in [self.gui.x0, self.gui.x1, self.gui.w]:
            adj = item.get_adjustment()
            adj.set_lower(0)
            adj.set_upper(self.selection.maxwidth)
            adj.set_step_increment(1)
            adj.set_page_increment(10)

        for item in [self.gui.y0, self.gui.y1, self.gui.h]:
            adj = item.get_adjustment()
            adj.set_lower(0)
            adj.set_upper(self.selection.maxheight)
            adj.set_step_increment(1)
            adj.set_page_increment(10)
            

        t = gtk.Table(4, 3)
        t.attach(create_label("x"), 0, 1, 0, 1, yoptions=gtk.SHRINK)
        t.attach(self.gui.x0,       1, 2, 0, 1, yoptions=gtk.SHRINK, xoptions=gtk.FILL)

        t.attach(create_label("y"), 2, 3, 0, 1, yoptions=gtk.SHRINK)
        t.attach(self.gui.y0,       3, 4, 0, 1, yoptions=gtk.SHRINK)

        t.attach(create_label("width"),  0, 1, 1, 2, yoptions=gtk.SHRINK)
        t.attach(self.gui.w,             1, 2, 1, 2, yoptions=gtk.SHRINK)

        t.attach(create_label("height"), 2, 3, 1, 2, yoptions=gtk.SHRINK)
        t.attach(self.gui.h,             3, 4, 1, 2, yoptions=gtk.SHRINK)

        self.gui.aspect_view = create_label("aspect")
        t.attach(self.gui.aspect_view, 0, 2, 2, 3, xoptions=gtk.FILL, yoptions=gtk.SHRINK)

        self.root = t


    def __connect(self):
        self.selection.listen(self.on_change)

        self.gui.x0.connect("value-changed", self.on_x0_change)
        self.gui.y0.connect("value-changed", self.on_y0_change)
        self.gui.w.connect("value-changed", self.on_width_change)
        self.gui.h.connect("value-changed", self.on_height_change)

    
    def on_change(self):
        x0, y0, w,  h  = self.selection.get_rectangle()
        x0, y0, x1, y1 = self.selection.get_coords()

        self.gui.x0.set_value(x0)
        self.gui.x1.set_value(x1)
        self.gui.y0.set_value(y0)
        self.gui.y1.set_value(y1)
        self.gui.w.set_value(w)
        self.gui.h.set_value(h)

        if h != 0:
            aspect = "aspect = %0.2f" % (w / float(h))
        else:
            aspect = "aspect = ?"
        
        self.gui.aspect_view.set_text(aspect)


    def on_x0_change(self, entry):
        self.selection.set_pos_x0(entry.get_value())


    def on_y0_change(self, entry):
        self.selection.set_pos_y0(entry.get_value())


    def on_width_change(self, entry):
        self.selection.set_width(entry.get_value())


    def on_height_change(self, entry):
        self.selection.set_height(entry.get_value())
