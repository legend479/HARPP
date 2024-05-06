"""
Hosts the definition of the group
"""
import random
from shapes import Shape
from object import Object
from typing import List, Optional
from constants import *
from typing import Union

class Group(Object):
    """
    Represents a group of objects.

    Attributes:
        objects (List[Shape]): The list of objects in the group.
        centroid (List[float]): The centroid of the group.
    """

    def __init__(self, objects: List[Shape]) -> None:
        """
        Initializes a Group object.

        Args:
            objects (List[Shape]): The list of objects in the group.
            parent (Optional[Group]): The parent group of the group (default: None).
        """
        self.objects = objects
        self.centroid = [sum([obj.centroid[0] for obj in objects]) / len(objects),
                         sum([obj.centroid[1] for obj in objects]) / len(objects)]

    def draw(self, window) -> None:
        """
        Draws the group on the specified window.

        Args:
            window: The window to draw the group on.
        """
        for obj in self.objects:
            obj.draw(window)

    def move(self, delta: tuple[int, int]) -> None:
        """
        Moves the group by the specified delta.

        Args:
            delta (tuple[int, int]): The amount to move the group in the x and y directions.
        """
        for obj in self.objects:
            obj.move(delta)

        self.centroid[0] += delta[0]
        self.centroid[1] += delta[1]

    def detect_selection(self, point: tuple[int, int]) -> Union[None, object]:
        """
        Detects if the specified point is within any object in the group.

        Args:
            point (tuple[int, int]): The point to check for selection.

        Returns:
            The selected object if found, None otherwise.
        """
        for obj in self.objects:
            sel = obj.detect_selection(point)
            if sel:
                return sel

        return None

    def get_duplicate(self) -> object:
        """
        Creates a duplicate of the group.

        Returns:
            A new Group object with duplicate objects.
        """
        duplicate_objects = [obj.get_duplicate() for obj in self.objects]
        return Group(duplicate_objects)

    def update_endpoints_randomly(self) -> None:
        """
        Updates the endpoints of the objects in the group randomly.
        """
        for obj in self.objects:
            obj.move((random.choice(RANDOM_CHOICES), random.choice(RANDOM_CHOICES)))
