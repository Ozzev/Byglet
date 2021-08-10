import pyglet.gl as pgl
import pyglet
import math


class Core:
    # SETTINGS
    MODE = None
    SIZE = [0, 0]
    TICKNESS = 1.0
    FILL = (255, 255, 255, 0)
    STROKE = (255, 255, 255, 255)

    # MODES
    BOTTOM_LEFT = 0
    TOP_LEFT = 1


class Basics:
    @staticmethod
    def setup(window, alpha_channel: bool = True):
        Core.WINDOW = window
        Core.SIZE = window.get_size()
        if alpha_channel:
            pgl.glEnable(pyglet.gl.GL_BLEND)
            pgl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    @staticmethod
    def set_mode(mode: int):
        Core.MODE = mode

    @staticmethod
    def tickness(tickness: float):
        Core.TICKNESS = tickness
        pgl.glLineWidth(tickness)

    @staticmethod
    def fill(color: tuple):
        Core.FILL = color

    @staticmethod
    def stroke(color: tuple):
        Core.STROKE = color

    @staticmethod
    def rect(x, y, w, h, mode=Core.MODE, tickness=Core.TICKNESS):
        if mode is None:
            mode = Core.MODE
        if mode == Core.TOP_LEFT:
            y = (Core.SIZE[1] - y)
            h = -h
        if tickness is not None:
            pgl.glLineWidth(tickness)
        pyglet.graphics.draw(
            4,
            pgl.GL_QUADS,
            (
                'v2f',
                [x, y, x + w, y, x + w, y + h, x, y + h]
            ),
            (
                'c4B',
                [c for i in range(4) for c in Core.FILL]
            )
        )
        pyglet.graphics.draw(
            4,
            pgl.GL_LINE_LOOP,
            (
                'v2f',
                [x, y, x + w, y, x + w, y + h, x, y + h]
            ),
            (
                'c4B',
                [c for i in range(4) for c in Core.STROKE]
            )
        )

    @staticmethod
    def circle(x, y, r, resolution=lambda r: r * 0.5, mode=Core.MODE, tickness=Core.TICKNESS):
        if mode is None:
            mode = Core.MODE
        if mode == Core.TOP_LEFT:
            y = (Core.SIZE[1] - y)
        if tickness is not None:
            pgl.glLineWidth(tickness)

        pgl.glBegin(pgl.GL_LINE_LOOP)
        for i in range(int(resolution(r))):
            ty = math.sin(2 * math.pi / resolution(r) * i)
            tx = math.cos(2 * math.pi / resolution(r) * i)
            pgl.glVertex2f(x + tx * r, y + ty * r)
        pgl.glEnd()

    @staticmethod
    def pivot_edit(points, pivot=(0, 0), angle=0, scale_mul=1):
        new = []
        for x, y in points:
            r = math.sqrt((pivot[0] - x) ** 2 + (pivot[1] - y) ** 2)
            t = [pivot[0] - x, pivot[1] - y]
            m = t[0] / t[1]
            t[0] = 1 if t[0] < 0 else -1
            t[1] = 1 if t[1] < 0 else -1
            a = math.atan(m)
            new.append([pivot[0] + t[0] * math.sin(a - math.radians(angle)) * r * scale_mul,
                        pivot[1] + t[1] * math.cos(a - math.radians(angle)) * r * scale_mul])
        return new


class Rect:
    def __init__(self, x, y, w, h, mode=Core.MODE, fill=Core.FILL, stroke=Core.STROKE, tickness=Core.TICKNESS):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mode = mode
        self.fill = fill
        self.stroke = stroke
        self.tickness = tickness

    def draw(self):
        Basics.rect(self.x, self.y, self.w, self.h, self.mode, self.tickness)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
