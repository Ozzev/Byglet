import pyglet.gl as pgl
import pyglet
import math


class Bbasics:
    # SETTINGS
    __SIZE = None
    __MODE = 0
    __TICKNESS = 1.0
    __FILL = [255, 255, 255, 0]
    __STROKE = [255, 255, 255, 255]

    # MODES
    BOTTOM_LEFT = 0
    TOP_LEFT = 1

    @staticmethod
    def setup(window, alpha_channel: bool = True):
        Bbasics.__WINDOW = window
        Bbasics.__SIZE = window.get_size()
        if alpha_channel:
            pgl.glEnable(pyglet.gl.GL_BLEND)
            pgl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
            print('a')

    @staticmethod
    def set_mode(mode: int):
        Bbasics.__MODE = mode

    @staticmethod
    def tickness(tickness: float):
        Bbasics.__TICKNESS = tickness
        pgl.glLineWidth(tickness)

    @staticmethod
    def fill(color: tuple):
        Bbasics.__FILL = color

    @staticmethod
    def stroke(color: tuple):
        Bbasics.__STROKE = color

    @staticmethod
    def rect(x, y, w, h, mode: int = None, tickness: float = None):
        if mode is None:
            mode = Bbasics.__MODE
        if mode == Bbasics.TOP_LEFT:
            y = (Bbasics.__SIZE[1] - y)
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
                [c for i in range(4) for c in Bbasics.__FILL]
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
                [c for i in range(4) for c in Bbasics.__STROKE]
            )
        )

    @staticmethod
    def circle(x, y, r, resolution=lambda r: r*0.5, mode: int = None, tickness: float = None):
        if mode is None:
            mode = Bbasics.__MODE
        if mode == Bbasics.TOP_LEFT:
            y = (Bbasics.__SIZE[1]-y)
        if tickness is not None:
            pgl.glLineWidth(tickness)

        pgl.glBegin(pgl.GL_LINE_LOOP)
        for i in range(int(resolution(r))):
            ty = math.sin(2*math.pi/resolution(r)*i)
            tx = math.cos(2*math.pi/resolution(r)*i)
            pgl.glVertex2f(x+tx*r, y+ty*r)
        pgl.glEnd()
