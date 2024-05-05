import PySimpleGUI as sg
from object import Object

DEFAULT_COLOR = (0,0,0)
CORNER_TYPE = ["pointed", "CURVY"]


class Shape(Object):
    def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
        super().__init__(height,width,centoid)
        self.color = DEFAULT_COLOR


class Line(Shape):
    def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
        super().__init__(height,width,centoid)
    pass

class Rectangle(Shape):
    def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
        super().__init__(height,width,centoid)
        self.type = 0
    pass

