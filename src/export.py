"""
Exporter module for exporting and importing drawing data to/from
 XML and ASCII text files.
"""
import xml.etree.ElementTree as ET
import sys
import os
from xml.dom import minidom
from shapes import Line, Rectangle
from group import Group
sys.path.append(os.getcwd())
class Exporter:
    """
    Exporter class to export the data to an xml file
    and ASCII text file
    """
    def __init__(self, drawables: list[object]):
        self.drawables = drawables

    def export_to_xml(self, file_path: str):
        """
        Exports the drawables to an XML file
        :param file_path:The file path to save the XML file
        :return:True if the export is successful, False otherwise
        """
        root = ET.Element('drawing')
        for drawable in self.drawables:
            root.append(self._convert_to_xml(drawable))
        # tree = ET.ElementTree(root)
        xml_str = ET.tostring(root, encoding='utf-8')
        xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
        try:
            with open(file_path, "w") as file:
                file.write(xml_pretty_str)
            return True  # Export successful
        except Exception as e:
            
            return False

    def import_from_xml(self, file_path: str):
        """
        Imports drawables from an XML file.
        :param file_path:The file path to the XML file.
        :return:A list of imported drawable objects.
        """
        drawables = []
        tree = ET.parse(file_path)
        root = tree.getroot()
        for elem in root:
            drawable = self._convert_from_xml(elem)
            if drawable:
                drawables.append(drawable)
        return drawables

    def export_to_file(self, file_path: str):
        """
        Exports the drawables to an ASCII text file.

        :param file_path:The file path to save the ASCII text file.

        :return: Nonetype
        """
        with open(file_path, "w") as file:
            for drawable in self.drawables:
                if isinstance(drawable, Line):
                    file.write(self._convert_line_to_string(drawable) + "\n")
                elif isinstance(drawable, Rectangle):
                    file.write(self._convert_rectangle_to_string(drawable) + "\n")
                elif isinstance(drawable, Group):
                    file.write("begin\n")
                    self._export_group_to_file(file, drawable)
                    file.write("end\n")

    def import_from_file(self, file_path: str):
        """
        Imports drawables from an ASCII text file
        :param file_path: The file path to the ASCII text file
        """
        drawables = []
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line == "begin":
                    group_objects, lines = self._import_group_from_file(lines)
                    drawables.append(Group(group_objects))
                else:
                    obj = self._convert_from_string(line)
                    if obj:
                        drawables.append(obj)
        return drawables

    def _convert_to_xml(self, drawable: object):
        """
        Converts a drawable object to XML format.
        :param drawable: The drawable object to convert
        :return:
        """
        if isinstance(drawable, Line):
            return self._convert_line_to_xml(drawable)
        elif isinstance(drawable, Rectangle):
            return self._convert_rectangle_to_xml(drawable)
        elif isinstance(drawable, Group):
            return self._convert_group_to_xml(drawable)

    def _convert_from_xml(self, elem):
        """
        Converts an XML element to a drawable object.
        :param elem:The XML element to convert.
        """
        if elem.tag == 'line':
            return self._convert_from_line_xml(elem)
        elif elem.tag == 'rectangle':
            return self._convert_from_rectangle_xml(elem)
        elif elem.tag == 'group':
            return self._convert_from_group_xml(elem)

    def _convert_line_to_xml(self, line: Line):
        """
        Converts a Line object to XML format.
        :param line: The Line object to convert.
        """
        line_elem = ET.Element('line')
        begin_elem = ET.SubElement(line_elem, 'begin')
        ET.SubElement(begin_elem, 'x').text =\
            str(line.start_point[0])
        ET.SubElement(begin_elem, 'y').text =\
            str(line.start_point[1])
        end_elem = ET.SubElement(line_elem, 'end')
        ET.SubElement(end_elem, 'x').text =\
            str(line.end_point[0])
        ET.SubElement(end_elem, 'y').text =\
            str(line.end_point[1])
        ET.SubElement(line_elem, 'color').text =\
            line.colour
        return line_elem

    def _convert_rectangle_to_xml(self, rectangle: Rectangle):
        """
        Converts a Rectangle object to XML format.

        :param rectangle:The Rectangle object to convert
        :return:The XML element representing the Rectangle object
        """
        rect_elem = ET.Element('rectangle')
        upper_left_elem = ET.SubElement(rect_elem, 'upper-left')
        ET.SubElement(upper_left_elem, 'x').text =\
            str(min(rectangle.start_point[0], rectangle.end_point[0]))
        ET.SubElement(upper_left_elem, 'y').text =\
            str(min(rectangle.start_point[1], rectangle.end_point[1]))
        lower_right_elem = ET.SubElement(rect_elem, 'lower-right')
        ET.SubElement(lower_right_elem, 'x').text =\
            str(max(rectangle.start_point[0], rectangle.end_point[0]))
        ET.SubElement(lower_right_elem, 'y').text =\
            str(max(rectangle.start_point[1], rectangle.end_point[1]))
        ET.SubElement(rect_elem, 'color').text =\
            rectangle.colour
        ET.SubElement(rect_elem, 'corner').text =\
            'Round' if rectangle.corner_type == 'Round' else 'Sharp'
        return rect_elem

    def _convert_group_to_xml(self, group: Group):
        """
        Converts a Group object to XML format.
        :param group:The Group object to convert
        """
        group_elem = ET.Element('group')
        for obj in group.objects:
            group_elem.append(self._convert_to_xml(obj))
        return group_elem

    def _convert_from_line_xml(self, elem):
        """
        Converts an XML element representing a Line object to a Line object.
        """
        start_x = int(elem.find('begin/x').text)
        start_y = int(elem.find('begin/y').text)
        end_x = int(elem.find('end/x').text)
        end_y = int(elem.find('end/y').text)
        color = elem.find('color').text
        return Line((start_x, start_y),
                    (end_x, end_y), color)

    def _convert_from_rectangle_xml(self, elem):
        """
        Converts an XML element representing a Rectangle object to a Rectangle object.
        """
        start_x = int(elem.find('upper-left/x').text)
        start_y = int(elem.find('upper-left/y').text)
        end_x = int(elem.find('lower-right/x').text)
        end_y = int(elem.find('lower-right/y').text)
        color = elem.find('color').text
        corner_type = elem.find('corner').text
        return Rectangle((start_x, start_y),
                         (end_x, end_y), color, corner_type)

    def _convert_from_group_xml(self, elem):
        """
        Converts an XML element representing a Group object to a Group object.
        :param elem:The XML element representing the Group object.
        """
        objects = []
        for child in elem:
            obj = self._convert_from_xml(child)
            if obj:
                objects.append(obj)
        return Group(objects)

    def _convert_line_to_string(self, line: Line):
        """
        Converts a Line object to a string.
        """
        return f"line {line.start_point[0]} {line.start_point[1]} {line.end_point[0]} {line.end_point[1]} {line.colour}"

    def _convert_rectangle_to_string(self, rectangle: Rectangle):
        """
               Converts a Rectangle object to a string.
        """
        corner_style = "r"\
            if rectangle.corner_type == "Round" else "Sharp"
        return f"rect {rectangle.start_point[0]} {rectangle.start_point[1]} {rectangle.end_point[0]} {rectangle.end_point[1]} {rectangle.colour} {corner_style}"

    def _convert_from_string(self, line: str):
        """
        Converts a string to a drawable object.
        """
        parts = line.split()
        if parts[0] == "line":
            start_x, start_y, end_x, end_y, color =\
                list(map(float, parts[1:5])) + [parts[5]]
            return Line((start_x, start_y),
                        (end_x, end_y), color)
        elif parts[0] == "rect":
            start_x, start_y, end_x, end_y, color, corner_style =\
                list(map(float, parts[1:5])) + [parts[5], parts[6]]
            return Rectangle((start_x, start_y),
                             (end_x, end_y), color, corner_style)
        return None

    def _export_group_to_file(self, file, group: Group):
        for obj in group.objects:
            if isinstance(obj, Line):
                file.write(self._convert_line_to_string(obj) + "\n")
            elif isinstance(obj, Rectangle):
                file.write(self._convert_rectangle_to_string(obj) + "\n")
            elif isinstance(obj, Group):
                file.write("begin\n")
                self._export_group_to_file(file, obj)
                file.write("end\n")
    def save_to_file(self, file_path='drawing.txt'):
        with open(file_path, "w") as file:
            for drawable in self.drawables:
                if isinstance(drawable, Line):
                    file.write(self._convert_line_to_string(drawable) + "\n")
                elif isinstance(drawable, Rectangle):
                    file.write(self._convert_rectangle_to_string(drawable) + "\n")
                elif isinstance(drawable, Group):
                    file.write("begin\n")
                    self._export_group_to_file(file, drawable)
                    file.write("end\n")

    def load_from_file(self, file_path='drawing.txt'):
        def process_group(lines, index):
            """
            helper method to recursively process group
            """
            group_objects = []
            while index < len(lines) and lines[index].strip() != "end":
                line = lines[index].strip()
                if line == "begin":
                    sub_group, index = process_group(lines, index + 1)
                    group_objects.append(sub_group)
                else:
                    obj = self._convert_from_string(line)
                    if obj:
                        group_objects.append(obj)
                index += 1
            return Group(group_objects), index

        drawables = []

        with open(file_path, "r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line == "begin":
                    group, i = process_group(lines, i + 1)
                    drawables.append(group)
                else:
                    obj = self._convert_from_string(line)
                    if obj:
                        drawables.append(obj)
                i += 1

        return drawables

    def _import_group_from_file(self, lines):
        """
        Imports a Group object from file lines.
        """
        group_objects = []
        for line in lines:
            line = line.strip()
            if line == "end":
                return group_objects, lines
            else:
                obj = self._convert_from_string(line)
                if obj:
                    group_objects.append(obj)
        return group_objects, lines
