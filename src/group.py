from typing import List, Optional
from shapes import Shape
from object import *
import random
from shapes import Line, Rectangle
class Group(Object):
    def __init__(self, objects: List[Shape], parent: Optional['Group'] = None):
        self.objects = objects
        self.centroid = [sum([obj.centroid[0] for obj in objects]) / len(objects) , sum([obj.centroid[1] for obj in objects]) / len(objects)]
        
        
        # self.parent = parent
        # self.children = []  # List of child groups
        # for obj in objects:
        #     if isinstance(obj, Group):
        #         obj.parent = self
        #         self.children.append(obj)
        # self.start_point = None
        # self.end_point = None
        # self.calculate_bounding_box()

    # def calculate_bounding_box(self):
    #     min_x = min(obj.start_point[0] for obj in self.objects)
    #     min_y = min(obj.start_point[1] for obj in self.objects)
    #     max_x = max(obj.end_point[0] for obj in self.objects)
    #     max_y = max(obj.end_point[1] for obj in self.objects)
    #     self.start_point = (min_x, min_y)
    #     self.end_point = (max_x, max_y)

    def draw(self, window):
        for obj in self.objects:
            # print(obj.colour)
            obj.draw(window)

    def move(self, delta: tuple[int, int]):
        # dx = new_point[0] - self.start_point[0]
        # dy = new_point[1] - self.start_point[1]
        # for obj in self.objects:
        #     obj.move((obj.start_point[0] + dx, obj.start_point[1] + dy))
        # self.calculate_bounding_box()
        # for child in self.children:
        #     child.move(self.start_point)

        for obj in self.objects:
            obj.move(delta)

        self.centroid[0] += delta[0]
        self.centroid[1] += delta[1]

    def detect_selection(self, point: tuple[int, int]):
        # x, y = point
        # if x <= self.end_point[0] and x >= self.start_point[0] and y <= self.start_point[1] and y >= self.end_point[1]:
        #     return self
        # return None

        for obj in self.objects:
            sel = obj.detect_selection(point)
            if sel:
                return sel

        return None
    
    def get_duplicate(self):
        duplicate_objects = [obj.get_duplicate() for obj in self.objects]
        return Group(duplicate_objects)
    def update_endpoints_randomly(self):
        a = [10, -10, -5, 5]  # Example values for random update
        for obj in self.objects:
            self._update_endpoints_recursive(obj, a)

    def _update_endpoints_recursive(self, obj, a):
        if isinstance(obj, (Line, Rectangle)):
            kk = random.choice(a)
            new_end_point = (obj.end_point[0] + kk, obj.end_point[1] + kk)
            obj.end_point = new_end_point
            new_start_point = (obj.start_point[0] + kk, obj.start_point[1] + kk)
            obj.start_point = new_start_point
        elif isinstance(obj, Group):
            for sub_obj in obj.objects:
                self._update_endpoints_recursive(sub_obj, a)