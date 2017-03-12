import sys
import gtk
import optparse

from dialog import MainWindow
from model.ImagePortion import ImagePortion


class ProgramError:
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def get_options(argv):
    parser = optparse.OptionParser(usage="""Usage: %prog [options] path""")

    parser.add_option(
        '-x', dest='x', type='int',
        help='x coordinate of rectangle'
    )

    parser.add_option(
        '-y', dest='y', type='int',
        help='y coordinate of rectangle'
    )

    parser.add_option(
        '-W', dest='w', type='int',
        help='width of rectangle'
    )

    parser.add_option(
        '-H', dest='h', type='int',
        help='height of rectangle'
    )

    parser.add_option(
        '-a', '--aspect', dest='aspect', type='float',
        help='aspect ratio, i.e. ratio width to height (positive number)'
    )

    parser.add_option(
        '--print-coords', dest='coords', action='store_true',
        help='print coordinates of rectangle, i.e. four integer numbers: x y x+w y+h'
    )

    parser.add_option(
        '--print-rect', dest='coords', action='store_false',
        help='print rectangle parametes, i.e. four integer numbers: x y w h'
    )

    options, args = parser.parse_args(argv)

    has_x = options.x is not None
    has_y = options.y is not None
    has_w = options.w is not None
    has_h = options.h is not None
    if has_x or has_y or has_w or has_h:
        if not (has_x and has_y and has_w and has_h):
            raise ProgramError('All options -x, -y, -W and -H must be given')

    if len(args) == 0:
        raise ProgramError("path not given")

    if len(args) > 1:
        raise ProgramError("more paths given, use only one, please")

    return options, args[0]


def main():
    try:
        options, path = get_options(sys.argv[1:])
    except ProgramError as err:
        print err
        return 1
    
    pixmap    = gtk.gdk.pixbuf_new_from_file(path)
    selection = ImagePortion(pixmap.get_width(), pixmap.get_height())
    if options.x is not None:
        selection.set_rectangle_unsafe(options.x, options.y, options.w, options.h)
    else:
        # temporarily
        selection.x0.set(100)
        selection.y0.set(200)
        selection.x1.set(100 + 640)
        selection.y1.set(200 + 480)
        selection.aspectratio = 640/480.

    app = MainWindow(path, pixmap, selection)
    app.run()

    return 0

if __name__ == '__main__':
    sys.exit(main())
