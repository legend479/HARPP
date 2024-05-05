import PySimpleGUI as sg
from object import Object
from collections import *
PEN_SIZE = 5
from typing import List
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
    def contains_point(self, point):
        x, y = point
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        return x1 <= x <= x2 and y1 <= y <= y2


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
    def contains_point(self, point):
        x, y = point
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        return x1 <= x <= x2 and y1 <= y <= y2

class Group(Shape):
    def __init__(self, objects: List[Shape]):
        self.objects = objects
        self.start_point = None
        self.end_point = None
        self.calculate_bounding_box()

    def calculate_bounding_box(self):
        min_x = min(obj.start_point[0] for obj in self.objects)
        min_y = min(obj.start_point[1] for obj in self.objects)
        max_x = max(obj.end_point[0] for obj in self.objects)
        max_y = max(obj.end_point[1] for obj in self.objects)
        self.start_point = (min_x, min_y)
        self.end_point = (max_x, max_y)

    def draw(self, window):
        for obj in self.objects:
            obj.draw(window)

    def move(self, dx, dy):
        for obj in self.objects:
            obj.move(dx, dy)
        self.calculate_bounding_box()