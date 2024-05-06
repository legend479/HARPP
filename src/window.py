"""
This module defines the Window class for managing the main window of the drawing program.
"""

import PySimpleGUI as sg
from constants import CANVAS_SIZE, BUTTON_SIZE, BIG_BUTTON_SIZE

# Description: Editor window for the user to
# interact with the program

class Window:
    """
    Manages the main window of the drawing program.
    Handles background settings, display, events, and closing.
    """

    def __init__(self, theme: str = "Default"):
        """
        Initializes the Window class.
        """
        self.theme = sg.theme(theme)
        self.canvas = sg.Graph(
            canvas_size=CANVAS_SIZE,
            graph_bottom_left=(0, 0),
            graph_top_right=CANVAS_SIZE,
            background_color="white",
            enable_events=True,
            key="-CANVAS-",
        )

        self.menubar = [
            ["File", ["Open", "Save", "Export", ["Export to XML"]]],
        ]

        self.topbar = [
            sg.Text("Shapes:"),
            sg.Button("Line", enable_events=True, key="-LINE-", auto_size_button=True),
            sg.Button("Rectangle", enable_events=True, key="-RECT-", auto_size_button=True),
            sg.Sizer(50, 1),
            sg.Text("Operations:"),
            sg.Button("Group", size=BUTTON_SIZE, enable_events=True, key="-GROUP-"),
            sg.Button("UnGroup", size=BUTTON_SIZE, enable_events=True, key="-UNGROUP-"),
            sg.Push(),
            sg.Button("Export to XML",
                      size=BIG_BUTTON_SIZE, enable_events=True, key="Export to XML"),
        ]

        self.bottombar = [
            sg.Button("Clear", size=BUTTON_SIZE, key="-CLEAR-", enable_events=True),
            sg.Push(),
            sg.Button("Save", size=BUTTON_SIZE),
            sg.Button("Open", size=BUTTON_SIZE, enable_events=True, key="Open"),
        ]

        self.layout = [
            [sg.Menu(self.menubar)],
            self.topbar,
            [self.canvas],
            self.bottombar,
        ]

        self.window = sg.Window(
            "HARPP Editor", layout=self.layout,
            margins=(0, 0), finalize=True, enable_close_attempted_event=True
        )

    def display(self):
        """
        Displays the window and handles events.
        """
        while True:
            event, _ = self.window.read()
            if event == sg.WIN_CLOSED:
                break
        self.window.close()

    def event(self):
        """
        Returns the current event on the window.
        """
        return self.window.read()

    def close(self):
        """
        Closes the window.
        """
        self.window.close()
