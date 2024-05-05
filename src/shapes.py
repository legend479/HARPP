import PySimpleGUI as sg
from object import Object

PEN_SIZE = 5

DEFAULT_COLOR = 'black'
CORNER_TYPE = ["pointed", "CURVY"]


class Shape(Object):
    # def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
    #     super().__init__(height,width,centoid)
    #     self.color = DEFAULT_COLOR

    def __init__(self, start_point, end_point):
        super().__init__(start_point, end_point)
        self.colour = DEFAULT_COLOR
        self.id = None



class Line(Shape):
    # def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
    #     super().__init__(height,width,centoid)
    # pass

    def __init__(self, start_point, end_point):
        super().__init__(start_point, end_point)

    def draw(self, window):
        self.id = window.canvas.draw_line(self.start_point, self.end_point, color = self.colour, width=PEN_SIZE)

    def move(self, new_point):
        '''
        For now, the top left corner will be where the mouse click happens
        '''
        self.start_point = new_point
        self.end_point = [new_point[0] + self.width, new_point[1] + self.height]
        self.centroid = [(self.start_point[0] + self.end_point[0]) / 2 , (self.start_point[1] + self.end_point[1]) / 2]

    def detect_selection(self, point):
        print("Selected")
        return self

class Rectangle(Shape):
    # def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
    #     super().__init__(height,width,centoid)
    #     self.type = 0
    # pass

    def __init__(self, start_point, end_point, corner_type = 's'):
        super().__init__(start_point, end_point)
        self.corner_type = corner_type

    def draw(self, window):
        self.id = window.canvas.draw_rectangle(self.start_point, self.end_point, line_color = self.colour, line_width=PEN_SIZE)

    def move(self, new_point):
        '''
        For now, the top left corner will be where the mouse click happens'''
        self.start_point = new_point
        self.end_point = new_point + [self.width, self.height]
        self.centroid = [(new_point[0] + self.end_point[0]) / 2 , (new_point[1] + self.end_point[1]) / 2]
