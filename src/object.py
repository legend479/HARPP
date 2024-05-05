import PySimpleGUI as sg
import datetime


class BoundingBox:
    def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
        self.hieght = height
        self.width = width
        self.centroid = centoid
        self.orientation = 0


class Object():
    # def __init__(self,height,width,centoid,id) -> None:
    #     self.bounding_box = BoundingBox(height,width,centoid)
    #     x,y = centoid
    #     self.id = id
    #     self.axis_alignment = ((x + width/2, y + width/2),(x - width/2, y - width/2))
    #     pass


    def __init__(self, start_point, end_point):
        # Calculate height, width and centroid
        # self.bounding_box
        self.width = end_point[0] - start_point[0]
        self.height = end_point[1] - start_point[1]
        self.centroid = [(start_point[0] + end_point[0]) / 2 , (start_point[1] + end_point[1]) / 2]
        self.start_point = start_point
        self.end_point = end_point
        
