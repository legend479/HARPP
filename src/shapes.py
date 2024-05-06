"""
This module houses all shapes relevant to drawing
"""
import math
from object import Object
from constants import DEFAULT_COLOR, DEFAULT_PEN_SIZE, ROUND_RADIUS, EPSILON
from typing import Optional, Union
import PySimpleGUI as sg


class Shape(Object):
    """
     This class is a parent class it sets the main
     template of all the classes making shapes
    """

    def __init__(self, start_point: list[int], end_point: list[int], pen_width: Optional[int] = DEFAULT_PEN_SIZE) -> None:
        super().__init__(start_point, end_point)
        self.color = DEFAULT_COLOR
        self.pen_width = pen_width
        self.selected = False

    def move(self, delta: list[int]) -> None:
        """
        Update line shape position
        """
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

    def __init__(self, start_point: tuple[int,int], end_point: tuple[int,int], color: str = DEFAULT_COLOR, pen_width: Optional[int] = DEFAULT_PEN_SIZE):
        super().__init__(start_point, end_point, pen_width)
        self.color = color
        diff = [start_point[0] - end_point[0], start_point[1] - end_point[1]]
        if diff[1] != 0:
            self.orientation = diff[0]/diff[1]
        else:
            self.orientation = INF

    def draw(self, window: sg.Window) -> None:
        """
            It draws the shape
        """
        color = "yellow" if self.selected else self.color
        self.id = window.canvas.draw_line(
            self.start_point, self.end_point, color=color, width=self.pen_width)

    def detect_selection(self, point: tuple[int, int]) -> Union[None, object]:
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
            a = self.end_point[1] - self.start_point[1]
            b = self.start_point[0] - self.end_point[0]
            c = self.start_point[1] * self.end_point[0] - self.start_point[0] * self.end_point[1]

            distance = abs(a * x + b * y + c) / ((a ** 2 + b ** 2) ** 0.5)

            if distance < EPSILON:
                return self
        return None

    def get_duplicate(self) -> object:
        x_offset = 20
        y_offset = 20
        start_point = [self.start_point[0] + x_offset, self.start_point[1] + y_offset]
        end_point = [self.end_point[0] + x_offset, self.end_point[1] + y_offset]
        return Line(start_point, end_point, self.color, self.pen_width)

class Rectangle(Shape):
    """
    A class representing a rectangle shape.

    Attributes:
        start_point (tuple[int, int]): The starting point of the rectangle.
        end_point (tuple[int, int]): The ending point of the rectangle.
        color (str): The color of the rectangle. Default is DEFAULT_COLOR.
        corner_type (str): The type of corners of the rectangle. Default is 'Sharp'.
    """

    def __init__(self, start_point: tuple[int, int], end_point: tuple[int, int], color: str = DEFAULT_COLOR, corner_type: Optional[str] = 'Sharp',pen_width: Optional[int] = DEFAULT_PEN_SIZE) -> None:
        super().__init__(start_point, end_point, pen_width=pen_width)
        self.corner_type = corner_type
        self.color = color

    def draw(self, window: sg.Window) -> None:
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
                           y1 - radius + radius * math.cos(angle)))

        for i in range(segments):
            angle = math.pi / 2 * i / segments
            points.append((x2 - radius + radius * math.sin(angle),
                           y1 - radius + radius * math.cos(angle)))

        for i in range(segments):
            angle = math.pi / 2 * (segments - i) / segments
            points.append((x2 - radius + radius * math.sin(angle),
                           y2 + radius - radius * math.cos(angle)))

        for i in range(segments):
            angle = math.pi / 2 * i / segments
            points.append((x1 + radius - radius * math.sin(angle),
                           y2 + radius - radius * math.cos(angle)))

        color = "yellow" if self.selected else self.color
        window.canvas.draw_polygon(
            points, fill_color="", line_color=color, line_width=self.pen_width)

    def detect_selection(self, point: tuple[int, int]) -> Union[None, object]:
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

    def get_duplicate(self) -> object:
        """
        Create a duplicate of the rectangle shape.

        Returns:
            Rectangle: A duplicate of the rectangle shape.
        """
        x_offset = 20
        y_offset = 20
        start_point = [self.start_point[0] + x_offset, self.start_point[1] + y_offset]
        end_point = [self.end_point[0] + x_offset, self.end_point[1] + y_offset]
        return Rectangle(start_point, end_point, self.color, self.corner_type, self.pen_width)