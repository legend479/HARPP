import PySimpleGUI as sg
# import datetime


class BoundingBox:
    def __init__(self, height: int, width: int, centoid: tuple[int, int]) -> None:
        self.hieght = height
        self.width = width
        self.centroid = centoid
        self.orientation = 0
        pass

class Object():
    def __init__(self,height,width,centoid,id) -> None:
        self.bounding_box = BoundingBox(height,width,centoid)
        x,y = centoid
        self.id = id
        self.axis_alignment = ((x + width/2, y + width/2),(x - width/2, y - width/2))
        pass