import tkinter as Tk
from tkinter import ttk
from .page import Template 

class LogContent(Template):
    def __init__(self, root, color_pallet={}):
        super().__init__(root, color_pallet)
        self._draw()

    def _draw(self):
        self._labels['logs'] = Tk.Label(
            self._main,
            anchor='w',
            name='logs',
            text='Logs: ',
            font=('Arial', 12, 'bold'),
            bg = self._color_pallet["label-background-enabled"],
            fg = self._color_pallet["label-foreground-enabled"]
        )
        self._labels['logs'].place(
            relx=0.01, rely=0.05, relwidth=0.2, relheight=0.07
        )
        self._entries['logs'] = Tk.Text(
            self._main,
            name='logscontent',
            bg = self._color_pallet["label-background-enabled"],
            fg = self._color_pallet["bottom-background"],
            font=("Arial", 10, 'bold'),
            highlightbackground = self._color_pallet["menu-background"],
            bd = 1
        )
        self._entries['logs'].place(
            relx=0.01, rely=0.12, relwidth = 0.98, relheight=0.75
        )
