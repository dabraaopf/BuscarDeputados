
import tkinter as Tk
from tkinter import ttk
from .page import Template 

class InfoContent(Template):
    def __init__(self, root, color_pallet={}):
        super().__init__(root, color_pallet)
        self._draw()

    def _draw(self):
        form_fields = ["name", "author", "version", "description"]
        top = 0.05
        size = 0.07
        padding = 0.01
        for field in form_fields:
            captilized = f'{field[0].upper()}{field[1:]}'
            self._labels[f'{field}'] = Tk.Label(
                self._main,
                anchor='e',
                name=f'{field}',
                text=f'{captilized}:',
                font=('Arial', 12, 'bold'),
                bg = self._color_pallet["label-background-enabled"],
                fg = self._color_pallet["label-foreground-enabled"]
            )
            self._labels[f'{field}'].place(
                relx=0.01, rely=top, relwidth=0.2, relheight=size
            )
            self._entries_values[f'{field}'] = Tk.StringVar()
            self._entries[f'{field}'] = Tk.Entry(
                self._main,
                name=f'{field}_content',
                textvariable = self._entries_values[f'{field}'],
                bg = self._color_pallet["label-background-enabled"],
                fg = self._color_pallet["bottom-background"],
                font=("Arial", 10, 'bold'),
                highlightbackground = self._color_pallet["menu-background"],
                bd = 1
            )
            self._entries[f'{field}'].place(
                relx=0.22, rely=top, relwidth = 0.48, relheight=size
            )
            top += size + padding


