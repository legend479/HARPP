from typing import List, Optional
from shapes import Shape
from object import *

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
            print(obj.colour)
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