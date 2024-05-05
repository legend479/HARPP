# Description: Editor window for the user to interact with the program

import PySimpleGUI as sg


class Window:

    def __init__(self, title="HARPP Editor"):
        
        self.canvas = sg.Graph(
            canvas_size=(800, 600),
            graph_bottom_left=(0, 0),
            graph_top_right=(800, 600),
            background_color="white",
            enable_events=True,
            key="canvas",
        )
        
        self.layout = [
            [sg.Text("HARPP Editor", size=(30, 1), justification="center")],
            [self.canvas],
            [sg.Text("Test", size=(30, 1), justification="center")],
        ]

        
        self.window = sg.Window(
            "HARPP Editor", layout=self.layout, margins=(0, 0))

    def display(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
        self.window.close()


