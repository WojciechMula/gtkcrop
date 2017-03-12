import pygtk
import gtk

from ImageWithSelection import Image
from PreviewSelection import PreviewSelection
from SelectionInputWidget import SelectionInputWidget
from AspectRatioInputWidget import AspectRatioInputWidget


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
        self.selection.notify()


    def __create_gui(self):
        # main window
        self.gui.root = gtk.Window(gtk.WINDOW_TOPLEVEL)
        caption = "File %s (%d x %d)" % (self.path, self.pixbuf.get_width(), self.pixbuf.get_height())
        self.gui.root.set_title(caption)
        self.gui.root.maximize()


        # menu
        self.gui.menu_exit = gtk.MenuItem("_Exit")
        self.gui.menu_preview = gtk.MenuItem("_Preview")
        self.gui.menu_commands = gtk.MenuItem("_Commands")
        menu = gtk.MenuBar()
        menu.append(self.gui.menu_exit)
        menu.append(self.gui.menu_commands)
        menu.append(self.gui.menu_preview)

        commands = gtk.Menu()
        self.gui.menu_commands.set_submenu(commands)
        self.gui.menu_select_whole_image   = gtk.MenuItem("Select _whole image")
        self.gui.menu_restore_aspect_ratio = gtk.MenuItem("Restore _aspect ratio")
        commands.append(self.gui.menu_select_whole_image)
        commands.append(self.gui.menu_restore_aspect_ratio)

        # main items
        self.image  = Image(self.pixbuf, self.selection)
        self.rect   = SelectionInputWidget(self.selection)
        self.aspect = AspectRatioInputWidget(self.selection, self.pixbuf.get_width(), self.pixbuf.get_height())
        self.gui.fixed_aspectratio = gtk.CheckButton("_Fixed aspect ratio")

        vbox = gtk.VBox()
        vbox.pack_start(self.rect.get_root(),       expand=False, fill=False)
        vbox.pack_start(self.gui.fixed_aspectratio, expand=False, fill=False)
        vbox.pack_start(self.aspect.get_root(),     expand=False, fill=False)

        hbox = gtk.HBox()
        hbox.pack_start(vbox, expand=False, fill=False)
        hbox.pack_end(self.image.get_root())

        # final setup
        main = gtk.VBox()
        main.pack_start(menu, expand=False, fill=False)
        main.pack_end(hbox)

        self.gui.root.add(main)
        self.gui.root.show_all()


    def __connect(self):
        self.gui.root.connect("delete_event", self.__root_delete_event)
        self.gui.menu_exit.connect("activate", self.__root_delete_event)
        self.gui.menu_preview.connect("button-press-event", self.__preview_event)
        self.gui.menu_preview.connect("activate", self.__preview_event)
        self.gui.fixed_aspectratio.connect("clicked", self.__use_fixed_aspectratio_event)
        self.gui.menu_restore_aspect_ratio.connect("activate", lambda _: self.__restore_aspect_ratio())
        self.gui.menu_select_whole_image.connect("activate", lambda _: self.__select_whole_image())


    def __root_delete_event(self, *args):
        gtk.main_quit()


    def __preview_event(self, *args):
        dialog = PreviewSelection(self.pixbuf, self.selection)
        dialog()

    def __use_fixed_aspectratio_event(self, button):
        self.selection.use_fixed_aspectratio(button.get_active())


    def __restore_aspect_ratio(self):
        self.aspect.reset()


    def __select_whole_image(self):
        self.selection.select_all()


    def run(self):
        self.gui.root.show()
        while True:
            try:
                gtk.main()
                return True
            except KeyboardInterrupt:
                print "Ctrl-C pressed"
                return False
            except:
                import traceback
                traceback.print_exc()
                return False

