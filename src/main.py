import PySimpleGUI as sg
import window as win
from shapes import *
from export import Exporter
from group import  Group
from constants import *
from typing import Union

def show_menu(cursor_pos: tuple[int, int]) -> Union[None, any]:
    layout = [
        [sg.Button("Edit")],
        [sg.Button("Delete")],
        [sg.Button("Copy&Paste")],
        [sg.Button("Cancel", button_color="red")]
    ]

    window = sg.Window("Menu", layout, location=cursor_pos,
                       no_titlebar=True, grab_anywhere=True)

    option = None
    while True:
        event, values = window.read()
        if event:
            option = event
            break
    window.close()
    return option


def show_edit_popup(drawable: object) -> None:
    layout = [
        [sg.Text("Edit Object")],
        [sg.Text("Color"), sg.InputText(drawable.colour, key="-COLOR-")],
        [sg.Text("Width"), sg.InputText(drawable.pen_width, key="-WIDTH-")],

        [sg.Text("Corner Type"), sg.DropDown(["Round", "Sharp"], default_value=drawable.corner_type,
                                             key="-TYPE-")] if isinstance(drawable, Rectangle) else [],

        [sg.Button("Save", key="Save"), sg.Button("Cancel", key="-CANCEL-")]
    ]

    window = sg.Window("Edit Object", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Save":
            drawable.colour = values["-COLOR-"]
            drawable.pen_width = values["-WIDTH-"]
            if isinstance(drawable, Rectangle):
                drawable.corner_type = values["-TYPE-"]
            break
        if event == "-CANCEL-":
            break

    window.close()


def update_canvas(window: sg.Window, drawables: list[object]) -> None:
    window.canvas.erase()
    for drawable in drawables:
        drawable.draw(window)


def main():
    window = win.Window(theme="Reddit")
    drawables = []  # Collection of all groups and individual objects.
    # drawing_line = False
    # drawing_rect = False
    c_map = {}
    selected_objects = []  # Stores the current objects
    window.canvas.bind("<Motion>", '-Motion-')
    window.canvas.bind("<Button-3>", '-RightClick-')
    group_mode = False
    ungroup_mode = False
    selected_indices = set()
    drawing_object = 0  # 0 refers to not drawing. 1 refers to line and 2 refers to rectangle
    start_pt = None
    groups = []
    end_pt = None
    selected_group = None
    selected_object = None
    unsaved_changes = False
    pen_width = DEFAULT_PEN_SIZE

    def update_colour_recursively(objects, c_map, color):
        for obj in objects:
            if isinstance(obj, Shape) and hasattr(obj, 'colour'):
                obj.colour = c_map.get(obj, color)
            elif isinstance(obj, Group):
                update_colour_recursively(obj.objects, c_map, color)
    try:
        while True:
            event, values = window.event()
            if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
                if unsaved_changes:
                    confirm = sg.popup_yes_no(
                        "You have unsaved changes. Do you want to continue?")
                    if confirm == "No":
                        continue
                    else:
                        break
                else:
                    break
            if event == sg.WIN_CLOSED :
                    break
            if event == "-LINEWIDTH-":
                pen_width = values["-LINEWIDTH-"]

            if event == "-GROUP-":
                group_mode = not group_mode
                if not group_mode:
                    new_friends = []
                    if len(selected_indices) > 0:
                        for friend in selected_indices:
                            obj = drawables[friend]
                            if isinstance(obj, Shape) and hasattr(obj, 'colour'):
                                obj.colour = c_map.get(obj, DEFAULT_COLOR)
                            elif isinstance(obj, Group):
                                update_colour_recursively(
                                    obj.objects, c_map, DEFAULT_COLOR)
                            new_friends.append(drawables[friend])

                        drawables.append(Group(new_friends))
                        li = list(selected_indices)
                        li = sorted(li)
                        li = reversed(li)

                        for friend in li:
                            drawables.pop(friend)

                        selected_indices = set()
                        c_map = {}
                        update_canvas(window, drawables)
                        unsaved_changes = True

                    window.window["-GROUP-"].update(text="Group")

            if group_mode:
                window.window["-GROUP-"].update(text="Done")
                if event == "-CANVAS-":
                    click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    for i, drawable in enumerate(drawables[::-1]):
                        if drawable.detect_selection(click_pt):

                            if i not in selected_indices:
                                selected_indices.add(i)
                                if (isinstance(drawable, Shape)
                                        and hasattr(drawable, 'colour')):
                                    drawable.colour = "yellow"
                                elif isinstance(drawable, Group):
                                    update_colour_recursively(
                                        drawable.objects, c_map, "yellow")

                            else:
                                selected_indices.remove(i)
                                obj = drawable
                                if isinstance(obj, Shape) and hasattr(obj, 'colour'):
                                    obj.colour = c_map.get(obj, DEFAULT_COLOR)
                                elif isinstance(obj, Group):
                                    update_colour_recursively(
                                        obj.objects, c_map, DEFAULT_COLOR)

                            update_canvas(window, drawables)
                            unsaved_changes = True
                            break

            elif ungroup_mode:
                if event == "-CANVAS-":
                    click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    for drawable in drawables[::-1]:
                        if drawable.detect_selection(click_pt):
                            selected_group = drawable
                            break
                    if isinstance(selected_group, Group):
                        ind = drawables.index(selected_group)
                        selected_group.update_endpoints_randomly()

                        drawables += drawables[ind].objects
                        drawables.pop(ind)
                        update_canvas(window, drawables)
                        unsaved_changes = True

                        selected_group = None
                        selected_object = None
                        ungroup_mode = False
                    else:
                        ungroup_mode = False
                        selected_group = None
                        selected_object = None

            else:
                if event == "-LINE-":
                    window.window["-LINE-"].update(button_color="light blue")
                    drawing_object = 1 if drawing_object != 1 else 0
                    start_pt = None
                    end_pt = None

                if event == "-RECT-":
                    window.window["-RECT-"].update(button_color="light blue")
                    drawing_object = 2 if drawing_object != 2 else 0
                    start_pt = None
                    end_pt = None
                if event == 'Export to XML':
                    exporter = Exporter(drawables)
                    file_path = sg.popup_get_file(
                        'Save As', save_as=True, file_types=(("XML Files", "*.xml"),))
                    if file_path:
                        exporter.export_to_xml(file_path+'.xml')

                if event == "-DELETE-":
                    if selected_group:
                        ind = drawable.index(selected_group)
                        drawable.remove(ind)
                        selected_group = None
                        selected_object = None

                if event == '-COPY-':
                    if selected_group:
                        drawables.append(selected_group.get_duplicate())

                if event == '-CANVAS-':
                    if drawing_object:
                        if start_pt is None:
                            start_pt = [values["-CANVAS-"]
                                        [0], values["-CANVAS-"][1]]
                        else:
                            end_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                            # window.canvas.draw_line(start_pt, end_pt, color=PEN_COLOR, width=pen_width)
                            match drawing_object:
                                case 1:
                                    window.window["-LINE-"].update(button_color=sg.theme_button_color())
                                    drawables.append(Line(start_pt, end_pt, pen_width=pen_width
                                                          ))
                                case 2:
                                    window.window["-RECT-"].update(button_color=sg.theme_button_color())
                                    drawables.append(Rectangle(start_pt, end_pt, pen_width=pen_width))
                            drawing_object = 0

                    else:
                        click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                        if not selected_group:
                            for drawable in drawables[::-1]:
                                selected_object = drawable.detect_selection(
                                    click_pt)
                                if selected_object:
                                    selected_group = drawable
                                    break

                        else:
                            delta = [values["-CANVAS-"][0] - selected_group.centroid[0],
                                    values["-CANVAS-"][1] - selected_group.centroid[1]]

                            selected_group.move(delta)
                            selected_group = None
                            selected_object = None
                            update_canvas(window, drawables)
                            unsaved_changes = True

            if selected_group:
                delta = [values["-CANVAS-"][0] - selected_group.centroid[0],
                        values["-CANVAS-"][1] - selected_group.centroid[1]]

                selected_group.move(delta)
                update_canvas(window, drawables)
                unsaved_changes = True

            if event == "-UNGROUP-":
                ungroup_mode = True

            if event == '-CANVAS--Motion-' and start_pt:
                update_canvas(window, drawables)
                unsaved_changes = True
                cursor_pos = values["-CANVAS-"]
                match drawing_object:
                    case 1:
                        window.canvas.draw_line(
                            start_pt, cursor_pos, color=PEN_COLOR, width=pen_width)
                    case 2:
                        window.canvas.draw_rectangle(
                            start_pt, cursor_pos, line_color=PEN_COLOR, line_width=pen_width)
            if event == "Save":
                save_path = sg.popup_get_file(
                    "Save Drawing", save_as=True, default_extension=".txt")
                if save_path:
                    exporter = Exporter(drawables)
                    exporter.save_to_file(save_path)
                    unsaved_changes = False

            if event == "Open":
                if unsaved_changes:                    
                    confirm = sg.popup_yes_no(
                        "You have unsaved changes. Do you want to continue?")
                    if confirm == "No":
                        continue
                    
                open_path = sg.popup_get_file(
                    "Open Drawing", default_extension=".txt")
                if open_path:                   
                    exporter = Exporter([])
                    try: 
                        drawables = exporter.load_from_file(open_path)
                    except Exception as e:
                        sg.popup_error(f"Error loading file: {e}")
                        continue
                    update_canvas(window, drawables)
                    unsaved_changes = False

            if event == "-CANVAS--RightClick-":
                click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                for i, drawable in enumerate(drawables[::-1]):
                    if (selected_object:=drawable.detect_selection(click_pt)):
                        cursor_pos = values["-CANVAS-"]
                        cursor_pos = window.window["-CANVAS-"].Widget.canvasx(
                            cursor_pos[0]), window.window["-CANVAS-"].Widget.canvasy(cursor_pos[1])
                        cursor_pos = (window.window["-CANVAS-"].Widget.winfo_rootx(
                        ) + cursor_pos[0], window.window["-CANVAS-"].Widget.winfo_rooty()
                            + CANVAS_SIZE[1] - cursor_pos[1])
                        option = show_menu(cursor_pos)
                        unsaved_changes = True

                        # HERE
                        if option == "Edit":
                            show_edit_popup(selected_object)
                        if option == "Delete":
                            drawables.pop(i)
                            update_canvas(window, drawables)
                            selected_group = None
                        if option == "Copy&Paste":
                            copy = drawable.get_duplicate()
                            drawables.append(copy)
                            update_canvas(window, drawables)
                            selected_group = copy
                        break

            if event == '-CLEAR-':
                drawables = []
                update_canvas(window, drawables)
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
