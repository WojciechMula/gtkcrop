import gtk


class Struct:
    pass


class AspectRatioInputWidget:

    def __init__(self, selection, width, height):
        self.width  = width
        self.height = height
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


        self.gui.num = gtk.SpinButton()
        self.gui.den = gtk.SpinButton()

        for item in [self.gui.num, self.gui.den]:
            adj = item.get_adjustment()
            adj.set_lower(0)
            adj.set_upper(max(self.width, self.height, 10000))
            adj.set_step_increment(1)
            adj.set_page_increment(10)

        self.gui.num.set_value(self.width)
        self.gui.den.set_value(self.height)

        hbox = gtk.HBox()
        hbox.add(self.gui.num)
        hbox.add(create_label("/"))
        hbox.add(self.gui.den)

        self.gui.aspect_view = create_label("")

        vbox = gtk.VBox()
        vbox.add(hbox)
        vbox.add(self.gui.aspect_view)

        self.root = vbox


    def __connect(self):
        self.gui.num.connect("value-changed", self.on_change)
        self.gui.den.connect("value-changed", self.on_change)
        self.on_change(None)

    
    def on_change(self, item):

        num = self.gui.num.get_value()
        den = self.gui.den.get_value()

        aspect = None

        if den != 0:
            aspect = (num / float(den))
            text = "aspect = %0.2f" % aspect
        else:
            text = "invalid input"
        
        self.gui.aspect_view.set_text(text)
        if aspect is not None:
            self.selection.set_aspect(aspect)

