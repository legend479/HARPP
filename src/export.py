import xml.etree.ElementTree as ET
from shapes import Line, Rectangle

class Exporter:
    def __init__(self, drawables: list[object]):
        self.drawables = drawables
        self.root = ET.Element('drawing')

    def export_to_xml(self, file_path: str):
        for drawable in self.drawables:
            self.root.append(self._convert_to_xml(drawable))

        tree = ET.ElementTree(self.root)
        tree.write(file_path)

    def _convert_to_xml(self, drawable: object):
        if isinstance(drawable, Line):
            return self._convert_line_to_xml(drawable)
        elif isinstance(drawable, Rectangle):
            return self._convert_rectangle_to_xml(drawable)
        # Add more cases for other drawable types

    def _convert_line_to_xml(self, line: Line):
        line_elem = ET.Element('line')
        begin_elem = ET.SubElement(line_elem, 'begin')
        ET.SubElement(begin_elem, 'x').text = str(line.start_point[0])
        ET.SubElement(begin_elem, 'y').text = str(line.start_point[1])
        end_elem = ET.SubElement(line_elem, 'end')
        ET.SubElement(end_elem, 'x').text = str(line.end_point[0])
        ET.SubElement(end_elem, 'y').text = str(line.end_point[1])
        ET.SubElement(line_elem, 'color').text = line.colour
        return line_elem

    def _convert_rectangle_to_xml(self, rectangle: Rectangle):
        rect_elem = ET.Element('rectangle')
        upper_left_elem = ET.SubElement(rect_elem, 'upper-left')
        ET.SubElement(upper_left_elem, 'x').text = str(min(rectangle.start_point[0], rectangle.end_point[0]))
        ET.SubElement(upper_left_elem, 'y').text = str(min(rectangle.start_point[1], rectangle.end_point[1]))
        lower_right_elem = ET.SubElement(rect_elem, 'lower-right')
        ET.SubElement(lower_right_elem, 'x').text = str(max(rectangle.start_point[0], rectangle.end_point[0]))
        ET.SubElement(lower_right_elem, 'y').text = str(max(rectangle.start_point[1], rectangle.end_point[1]))
        ET.SubElement(rect_elem, 'color').text = rectangle.colour
        ET.SubElement(rect_elem, 'corner').text = 'rounded' if rectangle.corner_type == 'r' else 'square'
        return rect_elem