from ImageComponent import Image as ImageComponent

class Image(ImageComponent):

    def __init__(self, pixbuf, selection):
        super(Image, self).__init__(pixbuf)
        self.selection = selection

    
    def world_to_window(self, x, y):
        return (
            self.dx + int(self.scale * x),
            self.dy + int(self.scale * y)
        )


    def custom_draw(self, window, style, gc):
        x = self.selection.x.get()
        y = self.selection.y.get()
        w = self.selection.w.get()
        h = self.selection.h.get()

        x0, y0 = self.world_to_window(x, y)
        x1, y1 = self.world_to_window(x + w, y + h)

        margin = 20

        def hline(x0, x1, y):
            window.draw_line(gc, x0, y, x1, y)

        def vline(x, y0, y1):
            window.draw_line(gc, x, y0, x, y1)

        if w > 2*margin and h > 2*margin:
            hline(x0, x1, y0 + margin)
            hline(x0, x1, y1 - margin)
            vline(x0 + margin, y0, y1)
            vline(x1 - margin, y0, y1)

        window.draw_rectangle(gc, False, x0, y0, x1 - x0, y1 - y0);
