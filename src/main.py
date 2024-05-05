from dependencies import *
import PySimpleGUI as sg
from export import Exporter


PEN_SIZE = 5
PEN_COLOR = 'black'    


def main():
    window = win.Window()
    drawables = [] # Collection of all groups and individual objects.
    # drawing_line = False
    # drawing_rect = False
    selected_objects = [] # Stores the current objects
    window.canvas.bind("<Motion>", '-Motion-')

    drawing_object = 0 # 0 refers to not drawing. 1 refers to line and 2 refers to rectangle
    start_pt = None
    end_pt = None
    selected_group = None
    selected_object = None
    
    while True:
        # for drawable in drawables:
        #     drawable.draw(window)
        #     print("YES")
        
        event, values = window.event()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
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
        if event == "-GROUP-":
            if selected_objects:
                group = Group(selected_objects)
                drawables.append(group)
                selected_objects.clear()

        if event == "-UNGROUP-":
            new_drawables = []
            for drawable in drawables:
                if isinstance(drawable, Group):
                    new_drawables.extend(drawable.objects)
                else:
                    new_drawables.append(drawable)
            drawables = new_drawables
        # if drawing_line and event == "-CANVAS-":
        #     if start_pt is None:
        #         start_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
        #     else:
        #         end_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
        #         # window.canvas.draw_line(start_pt, end_pt, color=PEN_COLOR, width=PEN_SIZE)
        #         drawables.append(Line(start_pt, end_pt))
        #         drawing_line = False
        
        # if drawing_rect and event == "-CANVAS-":
        #     if start_pt is None:
        #         start_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
        #     else:
        #         end_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
        #         # window.canvas.draw_rectangle(start_pt, end_pt, line_color=PEN_COLOR, line_width=PEN_SIZE)
        #         drawables.append(Rectangle(start_pt, end_pt))
        #         drawing_rect = False
        # Handle object selection
        if event == "-CANVAS-" and not drawing_object:
            cursor_pos = values["-CANVAS-"]
            for drawable in drawables:
                if drawable.contains_point(cursor_pos):
                    if drawable not in selected_objects:
                        selected_objects.append(drawable)
                    break
            else:
                selected_objects.clear()
        if event == '-CANVAS-':
            if drawing_object:
                if start_pt is None:
                    start_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                else:
                    end_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    # window.canvas.draw_line(start_pt, end_pt, color=PEN_COLOR, width=PEN_SIZE)
                    match drawing_object:
                        case 1:
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
                    selected_group.move(click_pt)
                    window.canvas.erase()
                    for drawable in drawables:
                        drawable.draw(window)


                pass
        
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
        
        if event == '-CLEAR-':
            drawables = []
            window.canvas.erase()
                
    
if __name__ == "__main__":
    main()
