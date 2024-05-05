import PySimpleGUI as sg
from object import Object
from collections import *
from typing import List
PEN_SIZE = 5
EPSILON = 10
INF = 100000000000000000000000000000
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

    def __init__(self, start_point: tuple[int,int], end_point: tuple[int,int]):
        super().__init__(start_point, end_point)
        diff = [start_point[0] - end_point[0], start_point[1] - end_point[1]]
        if diff[1] != 0:
            self.orientation = diff[0]/diff[1]
        else:
            self.orientation = INF

    def draw(self, window):
        self.id = window.canvas.draw_line(self.start_point, self.end_point, color = self.colour, width=PEN_SIZE)

    def move(self, new_point: tuple[int,int]):
        '''
        For now, the top left corner will be where the mouse click happens
        '''
        self.start_point = new_point
        self.end_point = [new_point[0] + self.width, new_point[1] + self.height]
        self.centroid = [(self.start_point[0] + self.end_point[0]) / 2 , (self.start_point[1] + self.end_point[1]) / 2]

    def detect_selection(self, point: tuple[int,int]):
        x,y = point
        if self.orientation == INF:
            if abs( y-self.start_point[1]) <= EPSILON and (x <= self.start_point[0] and x >= self.end_point[0] or x >= self.start_point[0] and x <= self.end_point[0]):
                return self
        else:
            if abs((self.orientation*y - x) -  (self.orientation*self.end_point[1] - self.end_point[0])) <= EPSILON:
                return self

        return None



class Rectangle(Shape):
    # def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
    #     super().__init__(height,width,centoid)
    #     self.type = 0
    # pass

    def __init__(self, start_point: tuple[int,int], end_point: tuple[int,int], corner_type = 's'):
        super().__init__(start_point, end_point)
        self.corner_type = corner_type

    def draw(self, window):
        self.id = window.canvas.draw_rectangle(self.start_point, self.end_point, line_color = self.colour, line_width=PEN_SIZE)

    def move(self, new_point: tuple[int,int]):
        '''
        For now, the top left corner will be where the mouse click happens'''
        self.start_point = new_point
        self.end_point = [new_point[0] + self.width, new_point[1] +  self.height]
        self.centroid = [(new_point[0] + self.end_point[0]) / 2 , (new_point[1] + self.end_point[1]) / 2]

    def detect_selection(self, point: tuple[int,int]):
        x,y = point
        if x <= self.end_point[0] and x >= self.start_point[0] and y <= self.start_point[1] and y >= self.end_point[1]:
            return self
        pass

#
# class Group(Shape):
#     def __init__(self, objects: List[Shape]):
#         self.objects = objects
#         self.start_point = None
#         self.end_point = None
#         self.calculate_bounding_box()
#
#     def calculate_bounding_box(self):
#         min_x = min(obj.start_point[0] for obj in self.objects)
#         min_y = min(obj.start_point[1] for obj in self.objects)
#         max_x = max(obj.end_point[0] for obj in self.objects)
#         max_y = max(obj.end_point[1] for obj in self.objects)
#         self.start_point = (min_x, min_y)
#         self.end_point = (max_x, max_y)
#
#     def draw(self, window):
#         for obj in self.objects:
#             obj.draw(window)
#
#     def move(self, dx: int, dy: int):
#         for obj in self.objects:
#             obj.move(dx, dy)
#         self.calculate_bounding_box()
#     def detect_selection(self, point: tuple[int,int]):
#         x,y = point
#         if x <= self.end_point[0] and x >= self.start_point[0] and y <= self.start_point[1] and y >= self.end_point[1]:
#             return self
#         pass
