
import tkinter as Tk
from tkinter import ttk
from .page import Template 

class InfoContent(Template):
    def __init__(self, root, color_pallet={}):
        super().__init__(root, color_pallet)
        self._draw()

    def _draw(self):
        print("should draw", type(self).__name__.lower())

