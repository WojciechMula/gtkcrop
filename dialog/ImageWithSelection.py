from ImageComponent import Image as ImageComponent
from SelectionView import *
from SelectionModifier import *

class Image(ImageComponent):

    def __init__(self, pixbuf, selection):
        super(Image, self).__init__(pixbuf)
        self.__connect_signals()

        self.selection        = selection
        self.selection_view   = SelectionView()
        self.selection_mod    = None
        self.selection_button = None

        self.selection.listen(lambda: self.model_refreshed())
        self.update_selection_view()


    def __connect_signals(self):
        item = self.gui.evb
        item.connect("size_allocate",        self.size_allocate_event)
        item.connect("motion_notify_event",  self.motion_event)
        item.connect("button_press_event",   self.button_press_event)
        item.connect("button_release_event", self.button_release_event)


    def update_selection_view(self):
        x0, y0, x1, y1 = self.selection.get_coords()

        def world_to_window(x, y):
            return (
                self.dx + int(self.scale * x),
                self.dy + int(self.scale * y)
            )

        x0, y0 = world_to_window(x0, y0)
        x1, y1 = world_to_window(x1, y1)

        self.selection_view.set(x0, y0, x1, y1)


    def window_to_world(self, x, y):
        return (
            int((x - self.dx)/self.scale),
            int((y - self.dy)/self.scale)
        )


    def custom_draw(self, window, style, gc):
        x0 = self.selection_view.x0
        y0 = self.selection_view.y0
        x1 = self.selection_view.x1
        y1 = self.selection_view.y1

        margin = self.selection_view.margin

        def hline(x0, x1, y):
            window.draw_line(gc, x0, y, x1, y)

        def vline(x, y0, y1):
            window.draw_line(gc, x, y0, x, y1)

        window.draw_pixbuf(gc, self.img_darkened, 0,  0, self.dx, self.dy, -1, -1)
        window.draw_pixbuf(gc, self.img_scaled,   x0 - self.dx, y0 - self.dy, x0, y0, x1 - x0, y1 - y0)

        if x1 - x0 > 2*margin and y1 - y0 > 2*margin:
            hline(x0, x1, y0 + margin)
            hline(x0, x1, y1 - margin)
            vline(x0 + margin, y0, y1)
            vline(x1 - margin, y0, y1)

        window.draw_rectangle(gc, False, x0, y0, x1 - x0, y1 - y0)


    # handlers
    def model_refreshed(self):
        w, h = self.get_image_size()

        self.update_selection_view()
        self.gui.image.queue_draw_area(self.dx, self.dy, w, h)


    def size_allocate_event(self, width, rect):
        self.update_selection_view()


    def motion_event(self, width, event):
        if not self.selection_mod:
            return

        x, y = self.window_to_world(event.x, event.y)
        self.selection_mod.update(x, y)


    def button_press_event(self, width, event):
        if self.selection_mod:
            return

        resize_mode = self.selection_view.classify(event.x, event.y)
        if resize_mode == INSIDE:
            SelectionClass = SelectionInside
        elif resize_mode == LEFT:
            SelectionClass = SelectionLeft
        elif resize_mode == RIGHT:
            SelectionClass = SelectionRight
        elif resize_mode == TOP:
            SelectionClass = SelectionTop
        elif resize_mode == BOTTOM:
            SelectionClass = SelectionBottom
        elif resize_mode == LEFT_TOP:
            SelectionClass = SelectionLeftTop
        elif resize_mode == RIGHT_TOP:
            SelectionClass = SelectionRightTop
        elif resize_mode == LEFT_BOTTOM:
            SelectionClass = SelectionLeftBottom
        elif resize_mode == RIGHT_BOTTOM:
            SelectionClass = SelectionRightBottom
        else:
            SelectionClass = None

        if SelectionClass:
            x, y = self.window_to_world(event.x, event.y)
            self.selection_mod    = SelectionClass(self.selection, x, y)
            self.selection_button = event.button
        else:
            self.selection_mod = None


    def button_release_event(self, width, event):
        if self.selection_mod and event.button == self.selection_button:
            self.selection_mod = None
