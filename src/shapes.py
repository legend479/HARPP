import PySimpleGUI as sg
from object import Object
from collections import *
import math
from constants import *


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
    
    def get_duplicate(self):
        x_offset = 20
        y_offset = 20
        start_point = [self.start_point[0] + x_offset, self.start_point[1] + y_offset]
        end_point = [self.end_point[0] + x_offset, self.end_point[1] + y_offset]
        return Line(start_point, end_point)

class Rectangle(Shape):
    """
    A class representing a rectangle shape.

    Attributes:
        start_point (tuple[int, int]): The starting point of the rectangle.
        end_point (tuple[int, int]): The ending point of the rectangle.
        color (str): The color of the rectangle. Default is DEFAULT_COLOR.
        corner_type (str): The type of corners of the rectangle. Default is 'Sharp'.
    """

    def __init__(self, start_point: tuple[int, int], end_point: tuple[int, int], color=DEFAULT_COLOR, corner_type='Sharp'):
        super().__init__(start_point, end_point)
        self.corner_type = corner_type

    def draw(self, window):
        """
        Draw the rectangle shape.

        Args:
            window: The window to draw the shape on.
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

    def detect_selection(self, point: tuple[int, int]):
        """
        Detect whether the click is inside the rectangle shape or not.

        Args:
            point (tuple[int, int]): The coordinates of the click.

        Returns:
            Rectangle: The rectangle shape if the click is inside, None otherwise.
        """
        x, y = point

        minx = min(self.start_point[0], self.end_point[0])
        miny = min(self.start_point[1], self.end_point[1])
        maxx = max(self.start_point[0], self.end_point[0])
        maxy = max(self.start_point[1], self.end_point[1])

        if x <= maxx and x >= minx and y <= maxy and y >= miny:
            return self
        return None

    def get_duplicate(self):
        """
        Create a duplicate of the rectangle shape.

        Returns:
            Rectangle: A duplicate of the rectangle shape.
        """
        x_offset = 20
        y_offset = 20
        start_point = [self.start_point[0] + x_offset, self.start_point[1] + y_offset]
        end_point = [self.end_point[0] + x_offset, self.end_point[1] + y_offset]
        return Rectangle(start_point, end_point)