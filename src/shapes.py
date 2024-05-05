import PySimpleGUI as sg
from object import Object
from collections import *
import math

PEN_SIZE = 5
EPSILON = 20
INF = 100000000000000000000000000000
DEFAULT_COLOR = 'black'
CORNER_TYPE = ["Sharp", "Rounded"]
ROUND_RADIUS = 10


class Shape(Object):
    """
     This class is a parent class it sets the main template of all the classes making shapes
    """

    def __init__(self, start_point, end_point):
        super().__init__(start_point, end_point)
        self.colour = DEFAULT_COLOR
        self.pen_width = PEN_SIZE
        self.id = None

    def move(self, delta):
        start_x, start_y = self.start_point
        end_x, end_y = self.end_point

        start_x += delta[0]
        start_y += delta[1]
        end_x += delta[0]
        end_y += delta[1]

        self.start_point = (start_x, start_y)
        self.end_point = (end_x, end_y)

        self.centroid[0] += delta[0]
        self.centroid[1] += delta[1]



class Line(Shape):
    """
        This is the line class it helps in making and storing the lines made.
    """

    def __init__(self, start_point: tuple[int,int], end_point: tuple[int,int], color = DEFAULT_COLOR):
        super().__init__(start_point, end_point)
        diff = [start_point[0] - end_point[0], start_point[1] - end_point[1]]
        if diff[1] != 0:
            self.orientation = diff[0]/diff[1]
        else:
            self.orientation = INF

    def draw(self, window):
        """
            It draws the shape
        """
        self.id = window.canvas.draw_line(
            self.start_point, self.end_point, color=self.colour, width=self.pen_width)

    # def move(self, new_point: tuple[int,int]):
    #     '''
    #     For now, the top left corner will be where the mouse click happens
    #     '''
    #     self.start_point = new_point
    #     self.end_point = [new_point[0] + self.width, new_point[1] + self.height]
    #     self.centroid = [(self.start_point[0] + self.end_point[0]) / 2 , (self.start_point[1] + self.end_point[1]) / 2]

    def detect_selection(self, point: tuple[int, int]):
        """
            It detects whether the click is inside the shape is or not
        """
        x,y = point
        minx = min(self.start_point[0], self.end_point[0])
        maxx = max(self.start_point[0], self.end_point[0])
        miny = min(self.start_point[1], self.end_point[1])
        maxy = max(self.start_point[1], self.end_point[1])
        if x<maxx and x>minx and y<maxy and y>miny:
            x, y = point
            # Calculate the line equation: Ax + By + C = 0
            A = self.end_point[1] - self.start_point[1]
            B = self.start_point[0] - self.end_point[0]
            C = self.start_point[1] * self.end_point[0] - self.start_point[0] * self.end_point[1]

            distance = abs(A * x + B * y + C) / ((A ** 2 + B ** 2) ** 0.5)

            if distance < EPSILON:
                return self
        return None


class Rectangle(Shape):

    def __init__(self, start_point: tuple[int, int], end_point: tuple[int, int], color = DEFAULT_COLOR, corner_type='Sharp'):
        super().__init__(start_point, end_point)
        self.corner_type = corner_type


    def draw(self, window):
        """
        It draws the shape
        """
        radius = 0 if self.corner_type == 'Sharp' else ROUND_RADIUS
        x1, y1 = self.start_point
        x2, y2 = self.end_point

        # Calculate the points for the rounded rectangle
        segments = 30  # Number of segments to approximate the circular arc
        points = []

        for i in range(segments):
            angle = math.pi / 2 * (segments - i) / segments
            points.append((x1 + radius - radius * math.sin(angle),
                        y1 + radius + radius * math.cos(angle)))

        for i in range(segments):
            angle = math.pi / 2 * i / segments
            points.append((x2 - radius + radius * math.sin(angle),
                        y1 + radius + radius * math.cos(angle)))

        for i in range(segments):
            angle = math.pi / 2 * (segments - i) / segments
            points.append((x2 - radius + radius * math.sin(angle),
                        y2 - radius - radius * math.cos(angle)))

        for i in range(segments):
            angle = math.pi / 2 * i / segments
            points.append((x1 + radius - radius * math.sin(angle),
                        y2 - radius - radius * math.cos(angle)))

        window.canvas.draw_polygon(
            points, fill_color="", line_color=self.colour, line_width=self.pen_width)

    # def move(self, new_point: tuple[int,int]):
    #     '''
    #     For now, the top left corner will be where the mouse click happens'''
    #     self.start_point = new_point
    #     self.end_point = [new_point[0] + self.width, new_point[1] +  self.height]
    #     self.centroid = [(new_point[0] + self.end_point[0]) / 2 , (new_point[1] + self.end_point[1]) / 2]

    def detect_selection(self, point: tuple[int, int]):
        """
            It detects whether the click is inside the shape is or not
        """
        x, y = point

        minx = min(self.start_point[0], self.end_point[0])
        miny = min(self.start_point[1], self.end_point[1])
        maxx = max(self.start_point[0], self.end_point[0])
        maxy = max(self.start_point[1], self.end_point[1])
        if x <= maxx and x >= minx and y <= maxy and y >= miny:
            return self
        return None
        pass
