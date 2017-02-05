import gtk

from ImageComponent import Image


class GUI:
    pass


class PreviewSelection(object):
    def __init__(self, pixbuf, selection):
        self.selection = selection
        self.pixbuf    = self.crop_image(pixbuf, selection)
        self.__setup()

    def __call__(self):
        try:
            self.dialog.maximize()
            self.dialog.run()
        finally:
            self.dialog.hide()

    def __setup(self):

        self.gui = GUI()

        self.gui.image   = Image(self.pixbuf, lambda: self.on_resize())
        self.gui.status  = gtk.Label()
        self.gui.status.set_alignment(0.0, 0.5)
        self.gui.status.set_padding(5, 5)

        self.dialog = gtk.Dialog("Preview %s" % self.selection, flags=gtk.DIALOG_MODAL)
        self.dialog.vbox.add(self.gui.image.get_root())
        self.dialog.vbox.pack_end(self.gui.status, expand=False, fill=False)
        self.dialog.show_all()


    def on_resize(self):
        w, h  = self.selection.get_dimensions()
        scale = self.gui.image.get_scale()
        if scale != 1.0:
            msg = "size %d x %d (showing at scale %0.3f)" % (w, h, scale)
        else:
            msg = "size %d x %d" % (w, h)
        
        self.gui.status.set_text(msg)


    def crop_image(self, pixbuf, selection):
        colorspace      = pixbuf.get_colorspace()
        has_alpha       = pixbuf.get_has_alpha()
        bits_per_sample = pixbuf.get_bits_per_sample()

        x, y, w, h = selection.get_rectangle()

        cropped = gtk.gdk.Pixbuf(colorspace, has_alpha, bits_per_sample, w, h)
        pixbuf.copy_area(x, y, w, h, cropped, 0, 0)

        return cropped
