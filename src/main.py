from dependencies import *
import PySimpleGUI as sg
import random



def show_menu(cursor_pos):
    layout = [
        [sg.Button("Edit", button_color=("grey", ""))],
        [sg.Button("Delete", button_color=("grey", ""))],
        [sg.Button("Copy&Paste", button_color=("grey", ""))],
        [sg.Button("Cancel", button_color=("grey", "black"))]
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


def show_edit_popup(drawable):
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


def update_canvas(window, drawables):
    window.canvas.erase()
    for drawable in drawables:
        drawable.draw(window)


def main():
    window = win.Window()
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

    def update_colour_recursively(objects, c_map, color):
        for obj in objects:
            if isinstance(obj, Shape) and hasattr(obj, 'colour'):
                obj.colour = c_map.get(obj, color)
            elif isinstance(obj, Group):
                update_colour_recursively(obj.objects, c_map, color)

    while True:
        event, values = window.event()
        print(event, values, group_mode, selected_objects)

        if event == sg.WIN_CLOSED:
            break
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
                        print(friend, drawables)
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
                for i, drawable in enumerate(drawables):
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
                for drawable in drawables:
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
                        # window.canvas.draw_line(start_pt, end_pt, color=PEN_COLOR, width=PEN_SIZE)
                        match drawing_object:
                            case 1:
                                print("TT")
                                window.window["-LINE-"].update(button_color="white")
                                drawables.append(Line(start_pt, end_pt))
                            case 2:
                                window.window["-RECT-"].update(button_color="white")
                                drawables.append(Rectangle(start_pt, end_pt))
                        drawing_object = 0

                else:
                    click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    if not selected_object:
                        for drawable in drawables:
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
                        start_pt, cursor_pos, color=PEN_COLOR, width=PEN_SIZE)
                case 2:
                    window.canvas.draw_rectangle(
                        start_pt, cursor_pos, line_color=PEN_COLOR, line_width=PEN_SIZE)
        if event == "Save":
            save_path = sg.popup_get_file(
                "Save Drawing", save_as=True, default_extension=".txt")
            if save_path:
                exporter = Exporter(drawables)
                exporter.save_to_file(save_path)
                unsaved_changes = False

        if event == "Open":
            open_path = sg.popup_get_file(
                "Open Drawing", default_extension=".txt")
            if open_path:
                print(open_path)
                if len(drawables) > 0:
                    if unsaved_changes:
                        confirm = sg.popup_yes_no(
                            "You have unsaved changes. Do you want to continue?")
                        if confirm == "No":
                            continue

                exporter = Exporter([])
                drawables = exporter.load_from_file(open_path)
                update_canvas(window, drawables)
                unsaved_changes = False

        if event == "-CANVAS--RightClick-":
            click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
            for i, drawable in enumerate(drawables):
                if (selected_object:=drawable.detect_selection(click_pt)):
                    cursor_pos = values["-CANVAS-"]
                    # convert the cursor position to the window coordinates
                    cursor_pos = window.window["-CANVAS-"].Widget.canvasx(
                        cursor_pos[0]), window.window["-CANVAS-"].Widget.canvasy(cursor_pos[1])
                    cursor_pos = (window.window["-CANVAS-"].Widget.winfo_rootx(
                    ) + cursor_pos[0], window.window["-CANVAS-"].Widget.winfo_rooty()
                        + 600 - cursor_pos[1])
                    option = show_menu(cursor_pos)
                    unsaved_changes = True

                    if option == "Edit":
                        show_edit_popup(selected_object)
                    if option == "Delete":
                        drawables.pop(i)
                        update_canvas(window, drawables)
                    if option == "Copy&Paste":
                        copy = drawable.get_duplicate()
                        drawables.append(copy)
                        update_canvas(window, drawables)
                        selected_group = copy
                    break

        if event == '-CLEAR-':
            drawables = []
            update_canvas(window, drawables)


if __name__ == "__main__":
    main()
