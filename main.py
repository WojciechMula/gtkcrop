import sys
import gtk

from dialog import MainWindow
from model.ImagePortion import ImagePortion

def help():
    print "usage"
    print "%s path-to-image" % sys.argv[0]

def main():
    if len(sys.argv) != 2:
        help()
        return 1
    else:
        path = sys.argv[1]
    
    pixmap    = gtk.gdk.pixbuf_new_from_file(path)
    selection = ImagePortion(pixmap.get_width(), pixmap.get_height())
    app = MainWindow(path, pixmap, selection)
    app.run()

    return 0

if __name__ == '__main__':
    sys.exit(main())
