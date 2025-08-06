import tkinter as Tk
from tkinter import ttk
from .page import Template 

class MainContent(Template):
    def __init__(self, root, color_pallet={}):
        super().__init__(root, color_pallet)
        self._draw()

    def _draw(self):
        self._labels['deputados'] = Tk.Label(
            self._main,
            anchor='w',
            name='deputados',
            text='Deputados: ',
            font=('Arial', 12, 'bold'),
            bg = self._color_pallet["label-background-enabled"],
            fg = self._color_pallet["label-foreground-enabled"]
        )
        self._labels['deputados'].place(
            relx=0.01, rely=0.05, relwidth=0.2, relheight=0.07
        )
        columns = ["col0", "col1", "col2", "col3", "col4"]
        self._entries['representatives'] = ttk.Treeview(
            self._main,
            name='representatives',
            columns=columns,
            show='headings'
        )
        self._entries['representatives'].place(
            relx=0.01, rely=0.12, relwidth = 0.98, relheight=0.75
        )
        self._buttons['search'] = Tk.Button(
            self._main,
            name='search',
            text='Buscar',
            bg = self._color_pallet["button-background-enabled"],
            fg = self._color_pallet["button-foreground-enabled"]
        )
        self._buttons['search'].place(
            relx=0.45, rely=0.9, relwidth=0.1, relheight=0.08
        )

    


