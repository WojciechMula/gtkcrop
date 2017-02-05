import pygtk
import gtk

from ImageWithSelection import Image
from PreviewSelection import PreviewSelection


class Struct:
    pass

class MainWindow:
    def __init__(self, path, pixbuf, selection):
        self.path      = path
        self.pixbuf    = pixbuf
        self.selection = selection
        self.__setup()


    def __setup(self):
        self.gui = Struct()
        self.__create_gui()
        self.__connect()


    def __create_gui(self):
        # main window
        self.gui.root = gtk.Window(gtk.WINDOW_TOPLEVEL)
        caption = "File %s (%d x %d)" % (self.path, self.pixbuf.get_width(), self.pixbuf.get_height())
        self.gui.root.set_title(caption)
        self.gui.root.resize(640, 480)

        # menu
        self.gui.menu_exit = gtk.MenuItem("_Exit")
        self.gui.menu_preview = gtk.MenuItem("_Preview")
        menu = gtk.MenuBar()
        menu.append(self.gui.menu_exit)
        menu.append(self.gui.menu_preview)

        # image view
        self.image = Image(self.pixbuf, self.selection)
        
        # final setup
        main = gtk.VBox()
        main.pack_start(menu, expand=False, fill=False)
        main.pack_end(self.image.get_root())

        self.gui.root.add(main)
        self.gui.root.show_all()


    def __connect(self):
        self.gui.root.connect("delete_event", self.__root_delete_event)
        self.gui.menu_exit.connect("activate", self.__root_delete_event)
        self.gui.menu_preview.connect("activate", self.__preview_event)


    def __root_delete_event(self, *args):
        gtk.main_quit()
 

    def __preview_event(self, *args):
        dialog = PreviewSelection(self.pixbuf, self.selection)
        dialog()


    def run(self):
        self.gui.root.show()
        while True:
            try:
                gtk.main()
                return
            except KeyboardInterrupt:
                print "Ctrl-C pressed"
                return
            except:
                import traceback
                traceback.print_exc()
                return

