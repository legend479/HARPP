import PySimpleGUI as sg
from object import Object

PEN_SIZE = 5

DEFAULT_COLOR = (0,0,0)
CORNER_TYPE = ["pointed", "CURVY"]


class Shape(Object):
    # def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
    #     super().__init__(height,width,centoid)
    #     self.color = DEFAULT_COLOR

    def __init__(self, start_point, end_point):
        super().__init__(start_point, end_point)
        self.colour = DEFAULT_COLOR



class Line(Shape):
    # def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
    #     super().__init__(height,width,centoid)
    # pass

    def __init__(self, start_point, end_point):
        super().__init__(start_point, end_point)

    def draw(self, window):
        window.canvas.draw_line(self.start_point, self.end_point, color = self.colour, width=PEN_SIZE)

    def move(self, dx, dy):
        self.start_point += [dx, dy]
        self.end_point += [dx, dy]

class Rectangle(Shape):
    # def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
    #     super().__init__(height,width,centoid)
    #     self.type = 0
    # pass

    def __init__(self, start_point, end_point, corner_type = 's'):
        super().__init__(start_point, end_point)
        self.corner_type = corner_type

    def draw(self, window):
        window.canvas.draw_rectangle(self.start_point, self.end_point, color = self.colour, width=PEN_SIZE)

    def move(self, dx, dy):
        self.start_point += [dx, dy]
        self.end_point += [dx, dy]
