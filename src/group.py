from typing import List, Optional
from shapes import Shape
from object import *
import random
from shapes import Line, Rectangle
class Group(Object):
    def __init__(self, objects: List[Shape], parent: Optional['Group'] = None):
        self.objects = objects
        self.centroid = [sum([obj.centroid[0] for obj in objects]) / len(objects) , sum([obj.centroid[1] for obj in objects]) / len(objects)]

    def draw(self, window):
        for obj in self.objects:
            # print(obj.colour)
            obj.draw(window)

    def move(self, delta: tuple[int, int]):

        for obj in self.objects:
            obj.move(delta)

        self.centroid[0] += delta[0]
        self.centroid[1] += delta[1]

    def detect_selection(self, point: tuple[int, int]):
        for obj in self.objects:
            sel = obj.detect_selection(point)
            if sel:
                return sel

        return None
    
    def get_duplicate(self):
        duplicate_objects = [obj.get_duplicate() for obj in self.objects]
        return Group(duplicate_objects)
    def update_endpoints_randomly(self):
        # a = [10, -10, -5, 5]  # Example values for random update
        for obj in self.objects:
            self._update_endpoints_recursive(obj, -10, 10)

    def _update_endpoints_recursive(self, obj, up_bound, low_bound):
        if isinstance(obj, Shape):
            kk = random.randint(up_bound, low_bound)
            new_end_point = (obj.end_point[0] + kk, obj.end_point[1] + kk)
            obj.end_point = new_end_point
            new_start_point = (obj.start_point[0] + kk, obj.start_point[1] + kk)
            obj.start_point = new_start_point
        elif isinstance(obj, Group):
            for sub_obj in obj.objects:
                self._update_endpoints_recursive(sub_obj, up_bound, low_bound)