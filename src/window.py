# Description: Editor window for the user to interact with the program

import pysimplegui as sg

class Window:
    INITIAL_LAYOUT = [
        [sg.Text("HARPP Editor", size=(30, 1), justification="center")],
        [sg.Text("Test", size=(30, 1), justification="center")],
    ]
    
    def __init__(self, layout=INITIAL_LAYOUT, title="HARPP Editor"):
        self.layout = layout
        self.window = sg.Window("HARPP Editor", layout=self.layout, margins=(0, 0))

    def display(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
        self.window.close()
    

if __name__ == "__main__":
    window = Window()
    window.display()