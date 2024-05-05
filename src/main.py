import window as win
import PySimpleGUI as sg

PEN_SIZE = 5
PEN_COLOR = 'black'

def main():
    window = win.Window()
    drawing_line = False
    while True:
        event, values = window.event()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == "-LINE-":
            drawing_line = True
            start_pt = None
            end_pt = None
            
        # if event == "-RECT-":
        #     print("Rect")
        
        if drawing_line and event == "-CANVAS-":
            if start_pt is None:
                start_pt = (values["-CANVAS-"][0], values["-CANVAS-"][1])
            else:
                end_pt = (values["-CANVAS-"][0], values["-CANVAS-"][1])
                window.canvas.draw_line(start_pt, end_pt, color=PEN_COLOR, width=PEN_SIZE)
                drawing_line = False
                
    
if __name__ == "__main__":
    main()
