import PySimpleGUI as sg
import window as win
from shapes import *
from export import Exporter
from group import Group
from constants import *
from typing import Union

class DrawingApp:
    def __init__(self):
        self.window = win.Window(theme="Reddit")
        self.drawables = []
        self.selected_objects = []
        self.group_mode = False
        self.ungroup_mode = False
        self.selected_indices = set()
        self.drawing_object = 0
        self.start_pt = None
        self.end_pt = None
        self.selected_group = None
        self.selected_object = None
        self.unsaved_changes = False
        self.pen_width = DEFAULT_PEN_SIZE

        self.setup_bindings()

    def setup_bindings(self):
        self.window.canvas.bind("<Motion>", '-Motion-')
        self.window.canvas.bind("<Button-3>", '-RightClick-')

    def run(self):
        while True:
            event, values = self.window.event()
            if self.handle_event(event, values):
                break

    def handle_event(self, event, values):
        event_handlers = {
            sg.WIN_CLOSE_ATTEMPTED_EVENT: self.handle_close_attempt,
            sg.WIN_CLOSED: lambda _: True,
            "-LINEWIDTH-": self.handle_line_width,
            "-GROUP-": self.handle_group,
            "-CANVAS-": self.handle_canvas_click,
            "-LINE-": self.handle_line_tool,
            "-RECT-": self.handle_rect_tool,
            "Export to XML": self.handle_export_xml,
            "-DELETE-": self.handle_delete,
            "-COPY-": self.handle_copy,
            "-UNGROUP-": self.handle_ungroup,
            '-CANVAS--Motion-': self.handle_canvas_motion,
            "Save": self.handle_save,
            "Open": self.handle_open,
            "-CANVAS--RightClick-": self.handle_right_click,
            '-CLEAR-': self.handle_clear,
        }

        handler = event_handlers.get(event)
        if handler:
            return handler(values)

    def handle_close_attempt(self, values):
        if self.unsaved_changes:
            confirm = sg.popup_yes_no("You have unsaved changes. Do you want to continue?")
            return confirm == "Yes"
        return True

    def handle_line_width(self, values):
        self.pen_width = values["-LINEWIDTH-"]

    def handle_group(self, values):
        self.group_mode = not self.group_mode
        self.ungroup_mode = False
        if not self.group_mode:
            new_grp = []
            if len(self.selected_indices) > 0:
                for indx in self.selected_indices:
                    obj = self.drawables[indx]
                    self.propagate_selection(obj, False)
                    new_grp.append(self.drawables[indx])

                self.drawables.append(Group(new_grp))
                li = sorted(list(self.selected_indices), reverse=True)

                for indx in li:
                    self.drawables.pop(indx)

                self.selected_indices = set()
                self.update_canvas()
                self.unsaved_changes = True

            self.window.window["-GROUP-"].update(text="Group")
        else:
            self.window.window["-GROUP-"].update(text="Done")

    def handle_canvas_click(self, values):
        if self.group_mode:
            click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
            for i, drawable in enumerate(self.drawables[::-1]):
                if drawable.detect_selection(click_pt):
                    if i not in self.selected_indices:
                        self.selected_indices.add(i)
                        self.propagate_selection(drawable, True)
                    else:
                        self.selected_indices.remove(i)
                        self.propagate_selection(drawable, False)
                    self.update_canvas()
                    self.unsaved_changes = True
                    break
        elif self.ungroup_mode:
            click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
            for drawable in self.drawables[::-1]:
                if drawable.detect_selection(click_pt):
                    self.selected_group = drawable
                    break
            if isinstance(self.selected_group, Group):
                ind = self.drawables.index(self.selected_group)
                self.selected_group.update_endpoints_randomly()
                self.drawables += self.drawables[ind].objects
                self.drawables.pop(ind)
                self.update_canvas()
                self.unsaved_changes = True
                self.selected_group = None
                self.selected_object = None
                self.ungroup_mode = False
            else:
                self.ungroup_mode = False
                self.selected_group = None
                self.selected_object = None
        else:
            if self.drawing_object:
                if self.start_pt is None:
                    self.start_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                else:
                    self.end_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    if self.drawing_object == 1:
                        self.window.window["-LINE-"].update(button_color=sg.theme_button_color())
                        self.drawables.append(Line(self.start_pt, self.end_pt, pen_width=self.pen_width))
                    elif self.drawing_object == 2:
                        self.window.window["-RECT-"].update(button_color=sg.theme_button_color())
                        self.drawables.append(Rectangle(self.start_pt, self.end_pt, pen_width=self.pen_width))
                    self.drawing_object = 0
            else:
                click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                if not self.selected_group:
                    for drawable in self.drawables[::-1]:
                        self.selected_object = drawable.detect_selection(click_pt)
                        if self.selected_object:
                            self.selected_group = drawable
                            break
                else:
                    delta = [values["-CANVAS-"][0] - self.selected_group.centroid[0],
                             values["-CANVAS-"][1] - self.selected_group.centroid[1]]
                    self.selected_group.move(delta)
                    self.selected_group = None
                    self.selected_object = None
                    self.update_canvas()
                    self.unsaved_changes = True

    def handle_line_tool(self, values):
        self.window.window["-LINE-"].update(button_color="light blue")
        self.drawing_object = 1 if self.drawing_object != 1 else 0
        self.start_pt = None
        self.end_pt = None

    def handle_rect_tool(self, values):
        self.window.window["-RECT-"].update(button_color="light blue")
        self.drawing_object = 2 if self.drawing_object != 2 else 0
        self.start_pt = None
        self.end_pt = None

    def handle_export_xml(self, values):
        exporter = Exporter(self.drawables)
        file_path = sg.popup_get_file('Save As', save_as=True, file_types=(("XML Files", "*.xml"),))
        if file_path:
            exporter.export_to_xml(file_path + '.xml')

    def handle_delete(self, values):
        if self.selected_group:
            ind = self.drawables.index(self.selected_group)
            self.drawables.pop(ind)
            self.selected_group = None
            self.selected_object = None
            self.update_canvas()
            self.unsaved_changes = True

    def handle_copy(self, values):
        if self.selected_group:
            self.drawables.append(self.selected_group.get_duplicate())
            self.update_canvas()
            self.unsaved_changes = True

    def handle_ungroup(self, values):
        if not self.group_mode: self.ungroup_mode = True

    def handle_canvas_motion(self, values):
        if self.start_pt:
            self.update_canvas()
            self.unsaved_changes = True
            cursor_pos = values["-CANVAS-"]
            if self.drawing_object == 1:
                self.window.canvas.draw_line(self.start_pt, cursor_pos, color=PEN_COLOR, width=self.pen_width)
            elif self.drawing_object == 2:
                self.window.canvas.draw_rectangle(self.start_pt, cursor_pos, line_color=PEN_COLOR, line_width=self.pen_width)
        if self.selected_group:
            # end_pt = (values["-CANVAS-"][0], values["-CANVAS-"][1])
            delta = (values["-CANVAS-"][0] - self.selected_group.centroid[0], values["-CANVAS-"][1]- self.selected_group.centroid[1])
            self.selected_group.move(delta)
            self.update_canvas()

    def handle_save(self, values):
        save_path = sg.popup_get_file("Save Drawing", save_as=True, default_extension=".txt")
        if save_path:
            exporter = Exporter(self.drawables)
            exporter.save_to_file(save_path)
            self.unsaved_changes = False

    def handle_open(self, values):
        if self.unsaved_changes:
            confirm = sg.popup_yes_no("You have unsaved changes. Do you want to continue?")
            if confirm == "No":
                return
        open_path = sg.popup_get_file("Open Drawing", default_extension=".txt")
        if open_path:
            exporter = Exporter([])
            try:
                self.drawables = exporter.load_from_file(open_path)
            except Exception as e:
                sg.popup_error(f"Error loading file: {e}")
                return
            self.update_canvas()
            self.unsaved_changes = False

    def handle_right_click(self, values):
        click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
        for i, drawable in enumerate(self.drawables[::-1]):
            if (selected_object := drawable.detect_selection(click_pt)):
                cursor_pos = values["-CANVAS-"]
                cursor_pos = self.window.window["-CANVAS-"].Widget.canvasx(cursor_pos[0]), self.window.window["-CANVAS-"].Widget.canvasy(cursor_pos[1])
                cursor_pos = (self.window.window["-CANVAS-"].Widget.winfo_rootx() + cursor_pos[0], 
                              self.window.window["-CANVAS-"].Widget.winfo_rooty() + CANVAS_SIZE[1] - cursor_pos[1])
                option = self.show_menu(cursor_pos)
                self.unsaved_changes = True

                if option == "Edit":
                    self.show_edit_popup(selected_object)
                if option == "Delete":
                    self.drawables.pop(len(self.drawables) - 1 - i)
                    self.update_canvas()
                    self.selected_group = None
                if option == "Copy&Paste":
                    copy = drawable.get_duplicate()
                    self.drawables.append(copy)
                    self.update_canvas()
                    self.selected_group = copy
                break

    def handle_clear(self, values):
        self.drawables = []
        self.update_canvas()
        self.unsaved_changes = True

    def update_canvas(self):
        self.window.canvas.erase()
        for drawable in self.drawables:
            drawable.draw(self.window)

    def propagate_selection(self, obj, selected):
        if isinstance(obj, Shape):
            obj.selected = selected
        elif isinstance(obj, Group):
            for c_obj in obj.objects:
                self.propagate_selection(c_obj, selected)

    def show_menu(self, cursor_pos):
        layout = [
            [sg.Button("Edit")],
            [sg.Button("Delete")],
            [sg.Button("Copy&Paste")],
            [sg.Button("Cancel", button_color="red")]
        ]

        window = sg.Window("Menu", layout, location=cursor_pos, no_titlebar=True, grab_anywhere=True)

        option = None
        while True:
            event, values = window.read()
            if event:
                option = event
                break
        window.close()
        return option

    def show_edit_popup(self, drawable):
        layout = [
            [sg.Text("Edit Object")],
            [sg.Text("Color"), sg.InputText(drawable.color, key="-COLOR-")],
            [sg.Text("Width"), sg.InputText(drawable.pen_width, key="-WIDTH-")],
            [sg.Text("Corner Type"), sg.DropDown(["Round", "Sharp"], default_value=drawable.corner_type, key="-TYPE-")] if isinstance(drawable, Rectangle) else [],
            [sg.Button("Save", key="Save"), sg.Button("Cancel", key="-CANCEL-")]
        ]

        window = sg.Window("Edit Object", layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Save":
                drawable.color = values["-COLOR-"]
                drawable.pen_width = values["-WIDTH-"]
                if isinstance(drawable, Rectangle):
                    drawable.corner_type = values["-TYPE-"]
                break
            if event == "-CANCEL-":
                break

        window.close()
        self.update_canvas()

def main():
    app = DrawingApp()
    try:
        app.run()
    except FileNotFoundError:
        sg.popup_error("File not found.")
    except PermissionError:
        sg.popup_error("Permission denied.")
    except IOError as e:
        sg.popup_error(f"IO error occurred: {e}")
    except Exception as e:
        sg.popup_error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()