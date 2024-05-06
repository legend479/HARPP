from typing import List, Optional
from shapes import Shape
from object import Object
import random
from typing import List, Optional

class Group(Object):
    """
    Represents a group of objects.

    Attributes:
        objects (List[Shape]): The list of objects in the group.
        centroid (List[float]): The centroid of the group.
    """

    def __init__(self, objects: List[Shape], parent: Optional['Group'] = None):
        """
        Initializes a Group object.

        Args:
            objects (List[Shape]): The list of objects in the group.
            parent (Optional[Group]): The parent group of the group (default: None).
        """
        self.objects = objects
        self.centroid = [sum([obj.centroid[0] for obj in objects]) / len(objects),
                         sum([obj.centroid[1] for obj in objects]) / len(objects)]

    def draw(self, window):
        """
        Draws the group on the specified window.

        Args:
            window: The window to draw the group on.
        """
        for obj in self.objects:
            obj.draw(window)

    def move(self, delta: tuple[int, int]):
        """
        Moves the group by the specified delta.

        Args:
            delta (tuple[int, int]): The amount to move the group in the x and y directions.
        """
        for obj in self.objects:
            obj.move(delta)

        self.centroid[0] += delta[0]
        self.centroid[1] += delta[1]

    def detect_selection(self, point: tuple[int, int]):
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

    def get_duplicate(self):
        """
        Creates a duplicate of the group.

        Returns:
            A new Group object with duplicate objects.
        """
        duplicate_objects = [obj.get_duplicate() for obj in self.objects]
        return Group(duplicate_objects)

    def update_endpoints_randomly(self):
        """
        Updates the endpoints of the objects in the group randomly.
        """
        for obj in self.objects:
            self._update_endpoints_recursive(obj, -10, 10)

    def _update_endpoints_recursive(self, obj, up_bound, low_bound):
        """
        Recursively updates the endpoints of the objects in the group.

        Args:
            obj: The object to update the endpoints for.
            up_bound: The upper bound for the random update.
            low_bound: The lower bound for the random update.
        """
        if isinstance(obj, Shape):
            kk = random.randint(up_bound, low_bound)
            new_end_point = (obj.end_point[0] + kk, obj.end_point[1] + kk)
            obj.end_point = new_end_point
            new_start_point = (obj.start_point[0] + kk, obj.start_point[1] + kk)
            obj.start_point = new_start_point
        elif isinstance(obj, Group):
            for sub_obj in obj.objects:
                self._update_endpoints_recursive(sub_obj, up_bound, low_bound)