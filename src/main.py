from dependencies import *
import PySimpleGUI as sg

PEN_SIZE = 5
PEN_COLOR = 'black'

def main():
    window = win.Window()
    drawables = [] # Collection of all groups and individual objects.
    # drawing_line = False
    # drawing_rect = False

    drawing_object = 0 # 0 refers to not drawing. 1 refers to line and 2 refers to rectangle
    while True:
        for drawable in drawables:
            drawable.draw(window)
            print("YES")
        
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

        if event == '-CANVAS-':
            if drawing_object:
                if start_pt is None:
                    start_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                else:
                    end_pt = [values["-CANVAS-"][0], values["-CANVAS-"][1]]
                    # window.canvas.draw_line(start_pt, end_pt, color=PEN_COLOR, width=PEN_SIZE)
                    if drawing_object == 1:
                        drawables.append(Line(start_pt, end_pt))
                    elif drawing_object == 2:
                        drawables.append(Rectangle(start_pt, end_pt))
                    drawing_object = 0

            else:
                # iterate through the drawables to detect selection clicks
                # do any recursive traversal

        
        window.canvas.erase() # So that window refreshes everytime, so that we can delete objects if we need to.
                
    
if __name__ == "__main__":
    main()
