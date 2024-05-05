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
            key="-CANVAS-",
        )

        self.topbar = [
            sg.Button("Line", size=(10, 1), enable_events=True, key="-LINE-"),
            sg.Button("Rect", size=(10, 1), enable_events=True, key="-RECT-"),
        ]

        self.bottombar = [
            sg.Button("Save", size=(10, 1)),
            sg.Button("Clear", size=(10, 1),key="-CLEAR-",enable_events=True),
        ]

        self.layout = [
            self.topbar,
            [self.canvas],
            self.bottombar,
        ]

        self.window = sg.Window(
            "HARPP Editor", layout=self.layout, margins=(0, 0), finalize=True,)

    def display(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
        self.window.close()

    def event(self):
        return self.window.read()

    def close(self):
        self.window.close()
