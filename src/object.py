import PySimpleGUI as sg

class Object():
    """
        This is the master class for both group and shapes. It provides them a basic structure to start with.
    """
    def __init__(self, start_point, end_point):

        self.width = end_point[0] - start_point[0]
        self.height = end_point[1] - start_point[1]
        self.centroid = [(start_point[0] + end_point[0]) / 2 , (start_point[1] + end_point[1]) / 2]
        self.start_point = start_point
        self.end_point = end_point


    def contains_point(self, point):
        raise NotImplementedError("Contains point method not implemented")