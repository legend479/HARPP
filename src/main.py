from dependencies import *
import PySimpleGUI as sg

PEN_SIZE = 5
PEN_COLOR = 'black'


def main():
    window = win.Window()
    drawables = [] # Collection of all groups and individual objects.
    # drawing_line = False
    # drawing_rect = False
    selected_objects = [] # Stores the current objects
    window.canvas.bind("<Motion>", '-Motion-')
    group_mode = False
    ungroup_mode = False
    selected_indices = set()
    drawing_object = 0 # 0 refers to not drawing. 1 refers to line and 2 refers to rectangle
    start_pt = None
    groups = []
    end_pt = None
    selected_group = None
    selected_object = None

    while True:
        # for drawable in drawables:
        #     drawable.draw(window)
        #     print("YES")

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
                        new_friends.append(drawables[friend])

                    drawables.append(Group(new_friends))
                    li = list(selected_indices)
                    li = sorted(li)
                    li = reversed(li)
                    # selected_indices = set(reversed(sorted(list(selected_indices))))
                    for friend in li:
                        print(friend, drawables)
                        drawables.pop(friend)
                    selected_indices = set()
                    window.canvas.erase()
                    for drawable in drawables:
                        drawable.draw(window)

                window.window["-GROUP-"].update(text = "Group")

        if group_mode:
            window.window["-GROUP-"].update(text = "Done")
            if event == "-CANVAS-":
                click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                for i, drawable in enumerate(drawables):
                    # selected_object = drawable.detect_selection(click_pt)
                    if drawable.detect_selection(click_pt):
                        if i not in selected_indices:
                            selected_indices.add(i)
                        else:
                            selected_indices.remove(i)

            # else:
            #     selected_group.move(click_pt)
            #     selected_group = None
            #     window.canvas.erase()
            #     for drawable in drawables:
            #         drawable.draw(window)
        
        elif ungroup_mode:
            if event == "-CANVAS-":
                click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                for drawable in drawables:
                    if drawable.detect_selection(click_pt):
                        selected_group = drawable
                        break
                if isinstance(selected_group, Group):
                    ind = drawables.index(selected_group)
                    drawables += drawables[ind].objects
                    drawables.pop(ind)
                    window.canvas.erase()
                    for drawable in drawables:
                        drawable.draw(window)
                    selected_group=None
                    selected_object= None
                    ungroup_mode = False

        else:
            if event == "-LINE-":
                # drawing_line = True
                # drawing_rect = False
                drawing_object = 1 if drawing_object != 1 else 0 # So that clicking the line button twice will exit the draw line state
                start_pt = None
                end_pt = None

            if event == "-RECT-":
                # drawing_line = False
                # drawing_rect = True
                drawing_object = 2 if drawing_object != 2 else 0
                start_pt = None
                end_pt = None
            if event == '-EXPORT-':
                exporter = Exporter(drawables)
                exporter.export_to_xml('drawing.xml')

            if event == "-DELETE-":
                if selected_group:
                    ind = drawable.index(selected_group)
                    drawable.remove(ind)
                    selected_group = None
                    selected_object = None

            if event == '-CANVAS-':
                if drawing_object:
                    if start_pt is None:
                        start_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    else:
                        end_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                        # window.canvas.draw_line(start_pt, end_pt, color=PEN_COLOR, width=PEN_SIZE)
                        match drawing_object:
                            case 1:
                                print("TT")
                                drawables.append(Line(start_pt, end_pt))
                            case 2:
                                drawables.append(Rectangle(start_pt, end_pt))
                        drawing_object = 0

                else:
                    click_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    if not selected_object:
                        for drawable in drawables:
                            selected_object = drawable.detect_selection(click_pt)
                            if selected_object:
                                selected_group = drawable
                                break

                    else:
                        delta = [values["-CANVAS-"][0] - selected_group.centroid[0], values["-CANVAS-"][1] - selected_group.centroid[1]]

                        selected_group.move(delta)
                        selected_group = None
                        selected_object = None
                        window.canvas.erase()
                        for drawable in drawables:
                            drawable.draw(window)
        
        if selected_group :
            delta = [values["-CANVAS-"][0] - selected_group.centroid[0], values["-CANVAS-"][1] - selected_group.centroid[1]]

            selected_group.move(delta)
            window.canvas.erase()
            for drawable in drawables:
                drawable.draw(window)
            
            

        if event == "-UNGROUP-":
            # new_drawables = []
            # for drawable in drawables:
            #     if isinstance(drawable, Group):
            #         new_drawables.extend(drawable.objects)
            #     else:
            #         new_drawables.append(drawable)
            # drawables = new_drawables


            # ind = drawables.index(selected_group)
            # drawables += drawables[ind].objects
            # drawables.pop(ind)
            # window.canvas.erase()
            # for drawable in drawables:
            #     drawable.draw(window)
            # selected_group=None
            # selected_object= None
            ungroup_mode = True

        if event == '-CANVAS--Motion-' and start_pt:
            window.canvas.erase()
            for drawable in drawables:
                drawable.draw(window)
            cursor_pos = values["-CANVAS-"]
            match drawing_object:
                case 1:
                    window.canvas.draw_line(start_pt, cursor_pos, color=PEN_COLOR, width=PEN_SIZE)
                case 2:
                    window.canvas.draw_rectangle(start_pt, cursor_pos, line_color=PEN_COLOR, line_width=PEN_SIZE)
        if event == "-SAVE-":
            save_path = sg.popup_get_file("Save Drawing", save_as=True, default_extension=".txt")
            if save_path:
                exporter = Exporter(drawables)
                exporter.save_to_file(save_path)

        if event == "-OPEN-":
            open_path = sg.popup_get_file("Open Drawing", default_extension=".txt")
            if open_path:
                print(open_path)
                if len(drawables) > 0:
                    confirm = sg.popup_yes_no("You have unsaved changes. Do you want to continue?")
                    if confirm == "No":
                        continue
                exporter = Exporter([])
                drawables = exporter.load_from_file(open_path)
                window.canvas.erase()
                print(drawables)
                for drawable in drawables:
                    drawable.draw(window)
        if event == '-CLEAR-':
            drawables = []
            window.canvas.erase()

if __name__ == "__main__":
    main()
