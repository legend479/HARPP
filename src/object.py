"""
Objects module defines all things on screen, group or individual, everything
"""

class Object():
    """
        This is the master class for both group and shapes.
         It provides them a basic structure to start with.
    """

    def __init__(self, start_point: list[int], end_point: list[int]) -> None:

        self.width = end_point[0] - start_point[0]
        self.height = end_point[1] - start_point[1]
        self.centroid = [(start_point[0] + end_point[0]) / 2,
                         (start_point[1] + end_point[1]) / 2]
        self.start_point = start_point
        self.end_point = end_point



