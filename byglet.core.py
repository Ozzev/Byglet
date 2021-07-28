import pyglet.gl as pgl
import pyglet


class Bbasics:
    # SETTINGS
    __SIZE = None
    __MODE = 0
    __TICKNESS = 1.0
    __FILL = (255, 255, 255, 255)
    __STROKE = (255, 255, 255, 255)

    # MODES
    BOTTOM_LEFT = 0
    TOP_LEFT = 1

    @staticmethod
    def setup(window):
        Bbasics.__WINDOW = window
        Bbasics.__SIZE = window.get_size()

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
        if tickness is not None:
            pgl.glLineWidth(tickness)

        if mode == 0:
            pyglet.graphics.draw(
                4,
                pgl.GL_QUADS,
                (
                    'v2f',
                    [x, y, x + w, y, x + w, y + h, x, y + h]
                ),
                (
                    'c4B',
                    [c for i in range(4) for c in Bbasics.__STROKE]
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

        elif mode == 1:
            pyglet.graphics.draw(
                4,
                pgl.GL_QUADS,
                (
                    'v2f',
                    [x, Bbasics.__SIZE[1] - y, x + w, Bbasics.__SIZE[1] - y, x + w,
                     Bbasics.__SIZE[1] - (y + h), x, Bbasics.__SIZE[1] - (y + h)]
                ),
                (
                    'c4B',
                    [c for i in range(4) for c in Bbasics.__FILL]
                )
            )
            pyglet.graphics.draw(
                4,
                pgl.GL_LINE_LOOP,
                ('v2f',
                 [x, Bbasics.__SIZE[1] - y, x + w, Bbasics.__SIZE[1] - y, x + w,
                  Bbasics.__SIZE[1] - (y + h), x, Bbasics.__SIZE[1] - (y + h)]
                 ),
                (
                    'c4B',
                    [c for i in range(4) for c in Bbasics.__STROKE]
                )
            )

    @staticmethod
    def circle():
        pass