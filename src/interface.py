import tkinter as Tk
from tkinter import ttk
from os import path, environ, getcwd
from time import time, sleep
from datetime import datetime
from json import loads, dumps
import logging
from PIL import Image
from .pages.main_content import MainContent
from .pages.log_content import LogContent
from .pages.info_content import InfoContent

class GUI():
    def __init__(self, root, config_file):
        self._root = root
        self._config_file = config_file
        self._log = None
        self._log_path = ""
        self._frames = {}
        self._buttons = {}
        self._labels = {}
        self._entries = {}
        self._entries_values = {}
        self._side_menu_options = {}
        self._configs = self._read_configs()
        self._color_pallet = self._get_colors()
        self._set_window()
        self._create_layout()
        self._pages = {
            "main" : MainContent(self._frames["content"], self._color_pallet),
            "details" : InfoContent(self._frames["content"], self._color_pallet),
            "log" : LogContent(self._frames["content"],self._color_pallet),
        }
        self._draw_menus()
        
    def _get_colors(self):
        return {
            "white" : "#FFFFFF",
            "black" : "#000000",
            "menu-background" : "#FECEAB",
            "menu-foreground" : "#FF847C",
            "button-background-enabled" : "#2A363B",
            "button-background-disabled" : "#DCEDC2",
            "button-foreground-enabled" : "#DCEDC2",
            "button-foreground-disabled" : "#2A363B",
            "label-background-enabled" : "#FFFFFF",
            "label-foreground-enabled" : "#FF847C",
            "label-background-disabled" : "#FFFFFF",
            "label-foregroud-disabled" : "#355C7D",
            "entry-background-enabled" : "#FFFFFF",
            "entry-foregroud-enabled" : "#FF847C",
            "entry-background-disabled" : "#99B898",
            "entry-foregroud-disabled" : "#355C7D",
            "entry-border" : "#2A363B",
            "bottom-background" : "#2A363B",
            "bottom-foreground" : "#C2B1E3",
            "header-background" : "#99B898",
            "header-foreground" : "#DCEDC2"
        }

    def _read_configs(self):
        log = self._get_logger()
        result = {}
        if not path.exists(self._config_file):
            return result 
        try:
            with open(self._config_file, 'r') as fl:
                data = fl.read()
            result = loads(data)
        except PermissionError as e:
            log.error(f'_read_configs: failed to open the config file') 
        except Exception as e:
            log.error(f'_read_configs: could not load de configs {type(e)}')
            result = {}
        finally:
            return result

    def _get_logger(self):
        if isinstance(self._log, logging.Logger):
            return self._log
        if self._log_path == "":
            self._log_path = path.join(getcwd(), "log.log")
        self._log = logging.getLogger("INTERFACE")
        logging.basicConfig(filename=self._log_path, level=logging.INFO)
        return self._log

    def _set_window(self):
        self._root.geometry("800x600+10+10")
        self._root.resizable(False, False)
        self._root.title(f".:: DAM :: {self._configs.get('name','')} ::.")

    def _create_layout(self):
        self._create_header()
        self._create_side_bar()
        self._create_bottom_bar()
        self._create_pages()

    def _create_header(self):
        self._frames["header"] = Tk.Frame(
            self._root, 
            name="header",
            bg = self._color_pallet["header-background"]
        )
        self._frames["header"].place(relx=0, rely=0, relheight=0.10, relwidth=1)
        self._labels["title"] = Tk.Label(
            self._frames["header"],
            name="title",
            anchor='center',
            bg=self._color_pallet["header-background"],
            fg=self._color_pallet["header-foreground"],
            text=f"{self._configs['name']}",
            font=('Arial', 18, 'bold')
        )
        self._labels["title"].place(
            relx=0.35, rely=0.2, relwidth=0.3, relheight=0.6
        )
        self._labels["username"] = Tk.Label(
            self._frames["header"],
            name="username",
            anchor='se',
            bg=self._color_pallet["header-background"],
            fg=self._color_pallet["header-foreground"],
            text=f"{environ['USER']}",
            font=('Arial', 10, 'bold')
        )
        self._labels["username"].place(
            relx=0.75, rely=0.7, relwidth=0.24, relheight=0.3
        )

    def _draw_menus(self):
        for menu in self._pages.keys():
            captilized = f"{menu[0].upper()}{menu[1:]}"
            self._side_menu_options[menu] = Tk.Label(
                self._frames['sidebar'],
                name=menu,
                text=f"{captilized}",
                fg=self._color_pallet['menu-foreground'],
                bg=self._color_pallet['menu-background'],
                font=('Arial', 14, 'bold')
            )
            self._side_menu_options[menu].bind('<Button-1>', self._load_page)
            self._side_menu_options[menu].bind('<Enter>', self._invert_colors)
            self._side_menu_options[menu].bind('<Leave>', self._invert_colors)

    def _create_side_bar(self):
        self._frames["sidebar"] = Tk.Frame(
            self._root, 
            name="sidebar",
            bg = self._color_pallet["menu-background"]
        )
        self._frames["sidebar"].place(
            relx=0.95, rely=0.1, relheight=0.85, relwidth=0.05
        )
        self._labels['mini_menu'] = Tk.Label(
            self._frames['sidebar'],
            name='mini_menu',
            anchor='center',
            text="::",
            fg=self._color_pallet['menu-foreground'],
            bg=self._color_pallet['menu-background'],
            font=('Arial', 12, 'bold')
        )
        self._labels['mini_menu'].place(
            relx=0.15, rely=0.01, relwidth=0.7, relheight=0.05
        )
        self._labels['mini_menu'].bind('<Button-1>', self._slide_side_bar_in)
        self._labels['mini_menu'].bind('<Enter>', self._invert_colors)
        self._labels['mini_menu'].bind('<Leave>', self._invert_colors)

    def _invert_colors(self, event):
        if event.type == Tk.EventType.Enter:
            event.widget.config(
                bg = self._color_pallet["menu-foreground"],
                fg = self._color_pallet["menu-background"]
            )
        elif event.type == Tk.EventType.Leave:
            event.widget.config(
                fg = self._color_pallet["menu-foreground"],
                bg = self._color_pallet["menu-background"]
            )

    def _load_page(self, event=None, name=""):
        if isinstance(event, Tk.Event):
            name = event.widget.winfo_name()
        for menu in self._pages.keys():
            self._pages[menu].visible((name == menu))

    def _slide_side_bar_in(self, event=None):
        # I can latter add a smooth effect, but so far it will be enough
        self._frames['sidebar'].unbind("<Leave>")
        self._frames['sidebar'].place_forget()
        self._labels['mini_menu'].place_forget()
        self._frames["sidebar"].place(
            relx=0.8, rely=0.1, relheight=0.85, relwidth=0.2
        )
        self._frames["content"].place_forget()
        self._frames["content"].place(
            relx=0, rely=0.1, relwidth = 0.80, relheight=0.85
        )
        top = 0.05
        for menu in self._pages.keys():
            self._side_menu_options[menu].place(
                relx=0.1, rely=top, relwidth=0.8, relheight=0.08
            )
            top += 0.1
        self._frames['sidebar'].bind("<Enter>", self._activate_leave)

    def _activate_leave(self, event=None):
        self._frames['sidebar'].bind("<Leave>", self._slide_side_bar_out)

    def _slide_side_bar_out(self, event=None):
        # I can latter add a smooth effect, but so far it will be enough
        self._labels['mini_menu'].place(
            relx=0.15, rely=0.01, relwidth=0.7, relheight=0.05
        )
        self._frames['sidebar'].place_forget()
        self._frames["sidebar"].place(
            relx=0.95, rely=0.1, relheight=0.85, relwidth=0.05
        )
        self._frames["content"].place_forget()
        self._frames["content"].place(
            relx=0, rely=0.1, relwidth = 0.95, relheight=0.85
        )
        for menu in self._pages.keys():
            self._side_menu_options[menu].place_forget()

    def _create_bottom_bar(self, links=[]):
        self._frames["footer"] = Tk.Frame(
            self._root, 
            name="footer",
            bg = self._color_pallet["bottom-background"]
        )
        self._frames["footer"].place(
            relx=0, rely=0.95, relheight=0.05, relwidth=1
        )
        self._labels['owner'] = Tk.Label(
            self._frames["footer"],
            name="owner",
            anchor='center',
            text="DAM",
            bg=self._color_pallet['bottom-background'],
            fg=self._color_pallet['bottom-foreground'],
            font=('Arial', 14, 'bold')
        )
        self._labels['owner'].place(
            relx=0.01, rely=0.1, relwidth=0.1, relheight=0.8
        )
        self._entries_values['short-text'] = Tk.StringVar()
        self._labels['short-text'] = Tk.Entry(
            self._frames["footer"],
            name="short-text",
            textvariable=self._entries_values['short-text'],
            bg=self._color_pallet['bottom-background'],
            fg=self._color_pallet['bottom-foreground'],
            bd=0,
            highlightbackground=self._color_pallet['bottom-background'],
            highlightthickness=1,
            highlightcolor=self._color_pallet['bottom-background'],
            font=('Arial', 10)
        )
        self._labels['short-text'].place(
            relx=0.11, rely=0.1, relwidth=0.75, relheight=0.8
        )

    def _create_pages(self):
        self._frames["content"] = Tk.Frame(
            self._root,
            name="content",
            bg = self._color_pallet["white"]
        )
        self._frames["content"].place(
            relx=0, rely=0.1, relwidth = 0.95, relheight=0.85
        )
            

        
