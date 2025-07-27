import tkinter as Tk
from tkinter import ttk

class Template():
    def __init__(self, root, color_pallet={}):
        self._root = root
        self._main = None
        self._buttons = {}
        self._labels = {}
        self._entries = {}
        self._entries_values = {}
        self._create_main()
        if len(color_pallet.keys()) > 0:
            self._color_pallet = color_pallet 
        else:
            self._color_pallet = self._get_colors()

    def _get_colors(self):
        return {
            'white' : "#ffffff",
            'black' : '#000000'
        }

    def visible(self, state):
        if state:
            self._main.place(
                relx=0, rely=0, relwidth=1, relheight=1
            )
        else:
            self._main.place_forget()

    def _create_main(self):
        self._main = Tk.Frame(
            self._root,
            name = type(self).__name__.lower(),
            bg = "white"
        )

    def bind_event(self, element_type, element_name, event_type, action):
        if element_type == "button":
            self._buttons[element_name].bind(event_type, action)
        elif element_type == "label":
            self._labels[element_name].bind(event_type, action)
        elif element_type == "entries":
            self._entries[element_name].bind(event_type, action)
