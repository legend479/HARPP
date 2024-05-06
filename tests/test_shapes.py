import os
import sys
from shapes import Line, Rectangle
from constants import DEFAULT_COLOR, DEFAULT_PEN_SIZE

sys.path.append(os.path.abspath('../src'))

def test_line_init():
    start_point = (0, 0)
    end_point = (10, 10)
    line = Line(start_point, end_point)
    assert line.start_point == start_point
    assert line.end_point == end_point
    assert line.color == DEFAULT_COLOR
    assert line.pen_width == DEFAULT_PEN_SIZE
    assert line.orientation == 1.0

def test_line_move():
    start_point = (0, 0)
    end_point = (10, 10)
    line = Line(start_point, end_point)
    delta = (5, 5)
    line.move(delta)
    assert line.start_point == (5, 5)
    assert line.end_point == (15, 15)
    assert tuple(line.centroid) == (float(10), float(10))

def test_line_detect_selection():
    start_point = (0, 0)
    end_point = (10, 10)
    line = Line(start_point, end_point)

    # Test a point on the line
    point = (5, 5)
    selected_line = line.detect_selection(point)
    assert selected_line == line

    # Test a point outside the line
    point = (20, 20)
    selected_line = line.detect_selection(point)
    assert selected_line is None

def test_line_get_duplicate():
    start_point = (0, 0)
    end_point = (10, 10)
    line = Line(start_point, end_point)
    duplicate_line = line.get_duplicate()
    assert tuple(duplicate_line.start_point) == (20, 20)
    assert tuple(duplicate_line.end_point) == (30, 30)

def test_rectangle_init():
    start_point = (0, 0)
    end_point = (10, 10)
    rect = Rectangle(start_point, end_point)
    assert rect.start_point == start_point
    assert rect.end_point == end_point
    assert rect.color == DEFAULT_COLOR
    assert rect.pen_width == DEFAULT_PEN_SIZE
    assert rect.corner_type == 'Sharp'

def test_rectangle_move():
    start_point = (0, 0)
    end_point = (10, 10)
    rect = Rectangle(start_point, end_point)
    delta = (5, 5)
    rect.move(delta)
    assert rect.start_point == (5, 5)
    assert rect.end_point == (15, 15)
    assert tuple(rect.centroid) == (10, 10)

def test_rectangle_detect_selection():
    start_point = (0, 0)
    end_point = (10, 10)
    rect = Rectangle(start_point, end_point)

    # Test a point inside the rectangle
    point = (5, 5)
    selected_rect = rect.detect_selection(point)
    assert selected_rect == rect

    # Test a point outside the rectangle
    point = (20, 20)
    selected_rect = rect.detect_selection(point)
    assert selected_rect is None

def test_rectangle_get_duplicate():
    start_point = (0, 0)
    end_point = (10, 10)
    rect = Rectangle(start_point, end_point)
    duplicate_rect = rect.get_duplicate()
    assert tuple(duplicate_rect.start_point) == (20, 20)
    assert tuple(duplicate_rect.end_point) == (30, 30)