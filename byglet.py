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
    TRANSFORM_MODE = 0

    # MODES
    WM_BOTTOM_LEFT = 0
    WM_TOP_LEFT = 1

    # TRANSFORM MODES
    TM_SINGLE = 0
    TM_STACK = 1


class Basics:
    @staticmethod
    def window(width, height, alpha_channel: bool = True, antialiasing: bool = True):
        if alpha_channel:
            pgl.glEnable(pyglet.gl.GL_BLEND)
            pgl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        try:
            config = pyglet.gl.Config(sample_buffers=1, samples=4)
            window = pyglet.window.Window(width, height, config=config)
        except pyglet.window.NoSuchConfigException:
            print("Multisampling not available.")
            window = pyglet.window.Window(width, height)

        Core.WINDOW = window
        Core.SIZE = window.get_size()
        return window

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
    def line(x1, y1, x2, y2, mode=Core.MODE, tickness=Core.TICKNESS):
        pyglet.graphics.draw(2, pgl.GL_LINES, ('v2f', [x1, y1, x2, y2]))

    @staticmethod
    def straight_line(x1, y1, x2, y2, mode=Core.MODE, tickness=Core.TICKNESS):
        diff = [x1 - x2, y1 - y2]
        if diff[0] == 0:
            nx1, nx2 = x1, x1
            ny1, ny2 = 0, Core.SIZE[1]
        else:
            m = diff[1] / diff[0]
            if m > 1:
                m = 1 / m
                ny1 = 0
                ny2 = Core.SIZE[1]
                f = lambda t: m * (t - y1) + x1
                nx1 = f(ny1)
                nx2 = f(ny2)
            else:
                nx1 = 0
                nx2 = Core.SIZE[0]
                f = lambda t: m * (t - x1) + y1
                ny1 = f(nx1)
                ny2 = f(nx2)
        pgl.glLineWidth(tickness)
        pyglet.graphics.draw(2, pgl.GL_LINES, ('v2f', [nx1, ny1, nx2, ny2]))
        pgl.glLineWidth(Core.TICKNESS)

    @staticmethod
    def circle(x, y, r, resolution=lambda r: r * 0.5, mode=Core.MODE, tickness=Core.TICKNESS):
        if mode is None:
            mode = Core.MODE
        if mode == Core.WM_TOP_LEFT:
            y = (Core.SIZE[1] - y)
        if tickness is not None:
            pgl.glLineWidth(tickness)

        pgl.glBegin(pgl.GL_LINE_LOOP)
        for i in range(int(resolution(r))):
            ty = math.sin(2 * math.pi / resolution(r) * i)
            tx = math.cos(2 * math.pi / resolution(r) * i)
            pgl.glVertex2f(x + tx * r, y + ty * r)
        pgl.glEnd()


class ShapeConfig:
    def __init__(self, mode=None, fill=None, stroke=None, tickness=None):
        self.mode = mode if mode is not None else Core.MODE
        self.fill = fill if fill is not None else Core.FILL
        self.stroke = stroke if stroke is not None else Core.STROKE
        self.tickness = tickness if tickness is not None else Core.TICKNESS


class Transform:
    @staticmethod
    def rotate(points, angle, pivot=(0, 0)):
        return Transform.pivot_edit(points, pivot=pivot, angle=angle, scale_mul=(1, 1))

    @staticmethod
    def scale(points, scale_mul=(1, 1), pivot=(0, 0)):
        return Transform.pivot_edit(points, pivot=pivot, angle=0, scale_mul=scale_mul)

    @staticmethod
    def pivot_edit(points, pivot=(0, 0), angle=0, scale_mul: tuple = (1, 1)):
        new = []
        it = iter(points)
        for x, y in zip(it, it):
            r = math.sqrt((pivot[0] - x) ** 2 + (pivot[1] - y) ** 2)
            diff = [pivot[0] - x, pivot[1] - y]
            if diff[0] == 0:
                a = math.pi / 2 * (1 if diff[1] < 0 else -1)
            else:
                m = diff[1] / diff[0]
                a = math.atan(m)
            new.extend([pivot[0] + (-1 if diff[0] > 0 else 1) * math.cos(a - math.radians(angle)) * r * scale_mul[0],
                        pivot[1] + (-1 if diff[0] > 0 else 1) * math.sin(a - math.radians(angle)) * r * scale_mul[1]])
        return new


class Path(ShapeConfig):
    def __init__(self, points: list, closed=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert ((len(points) / 2).is_integer())
        self.__i_points = points
        self.__points = points
        self.__closed = closed
        self.__center = self.get_center()

    def draw(self):
        pgl.glLineWidth(self.tickness)
        pyglet.graphics.draw(len(self.__points) // 2, pgl.GL_LINE_LOOP if self.__closed else pgl.GL_LINE_STRIP,
                             ('v2f', self.__points))
        pgl.glLineWidth(Core.TICKNESS)

    def get_center(self):
        xs, ys = 0, 0
        it = iter(self.__points)
        for p in zip(it, it):
            xs += p[0]
            ys += p[1]
        return xs / (len(self.__points) // 2), ys / (len(self.__points) // 2)

    def get_points(self):
        return self.__points[:]

    def rotate(self, angle, pivot=None, transform_mode=None):
        tmode = Core.TRANSFORM_MODE if transform_mode is None else transform_mode
        self.__points = Transform.rotate(self.__points if tmode != Core.TM_SINGLE else self.__i_points, angle,
                                         self.__center if pivot is None else pivot)

    def scale(self, scale_mul: tuple, pivot=None, transform_mode=None):
        tmode = Core.TRANSFORM_MODE if transform_mode is None else transform_mode
        self.__points = Transform.scale(self.__points if tmode != Core.TM_SINGLE else self.__i_points, scale_mul,
                                        self.__center if pivot is None else pivot)

    def pivot_edit(self, pivot=None, angle=0, scale_mul: tuple = (1, 1), transform_mode=None):
        tmode = Core.TRANSFORM_MODE if transform_mode is None else transform_mode
        self.__points = Transform.pivot_edit(self.__points if tmode != Core.TM_SINGLE else self.__i_points,
                                             self.__center if pivot is None else pivot, angle, scale_mul)


class Rect(Path):
    def __init__(self, x, y, w, h, *args, **kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        super().__init__([x, y, x + w, y, x + w, y + h, x, y + h], closed=True, *args, **kwargs)

    def draw(self):
        super().draw()

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_path(self):
        return super()


class Line(Path):
    def __init__(self, x1, y1, x2, y2, segment=True, *args, **kwargs):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.__segment = segment
        if not segment:
            diff = [x1 - x2, y1 - y2]
            if diff[0] == 0:
                nx1, nx2 = x1, x1
                ny1, ny2 = 0, Core.SIZE[1]
            else:
                m = diff[1] / diff[0]
                if m > 1:
                    m = 1 / m
                    ny1 = 0
                    ny2 = Core.SIZE[1]
                    f = lambda t: m * (t - y1) + x1
                    nx1 = f(ny1)
                    nx2 = f(ny2)
                else:
                    nx1 = 0
                    nx2 = Core.SIZE[0]
                    f = lambda t: m * (t - x1) + y1
                    ny1 = f(nx1)
                    ny2 = f(nx2)
            super().__init__([nx1, ny1, nx2, ny2], *args, **kwargs)
        else:
            super().__init__([x1, y1, x2, y2], *args, **kwargs)

    def draw(self):
        super().draw()

    @staticmethod
    def intersection(l1: 'Line', l2: 'Line'):
        diff1 = [l1.x1 - l1.x2, l1.y1 - l1.y2]
        diff2 = [l2.x1 - l2.x2, l2.y1 - l2.y2]
        m1 = diff1[1] / diff1[0] if diff1[0] != 0 else None
        m2 = diff2[1] / diff2[0] if diff2[0] != 0 else None
        if m2 is None:
            f = m1 * (l2.x1 - l1.x1) + l1.y1
            return l2.x1, f
        elif m1 is None:
            f = m2 * (l1.x1 - l2.x1) + l2.y1
            return l1.x1, f
        else:
            q1 = -m1 * l1.x1 + l1.y1
            q2 = -m2 * l2.x1 + l2.y1
            tx = (q2 - q1) / (m1 - m2)
            ty = m1 * (tx - l1.x1) + l1.y1
            return tx, ty
