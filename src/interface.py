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
            "label-foregroud-enabled" : "#FF847C",
            "label-background-disabled" : "#FFFFFF",
            "label-foregroud-disabled" : "#355C7D",
            "entry-background-enabled" : "#FFFFFF",
            "entry-foregroud-enabled" : "#FF847C",
            "entry-background-disabled" : "#99B898",
            "entry-foregroud-disabled" : "#355C7D",
            "entry-border" : "#2A363B",
            "bottom-background" : "#2A363B",
            "bottom-foreground" : "#E84A5F",
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
        self._create_side_bar(slide=True)
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

    def _create_side_bar(self, menus=["Main","Logs","Details"], slide=False):
        self._frames["sidebar"] = Tk.Frame(
            self._root, 
            name="sidebar",
            bg = self._color_pallet["menu-background"]
        )
        self._frames["sidebar"].place(
            relx=0.8, rely=0.1, relheight=0.85, relwidth=0.2
        )
        top = 0.05
        for menu in menus:
            menu_lower = menu.lower()
            self._side_menu_options[menu_lower] = Tk.Label(
                self._frames['sidebar'],
                name=menu_lower,
                text=menu,
                fg=self._color_pallet['menu-foreground'],
                bg=self._color_pallet['menu-background'],
                font=('Arial', 14, 'bold')
            )
            self._labels[menu_lower].place(
                relx=0.1, rely=top, relwidth=0.8, relheight=0.08
            )
            top += 0.1

        self._labels['mini_menu'] = Tk.Label(
            self._frames['sidebar'],
            name='mini_menu',
            anchor='center',
            text=":::",
            fg=self._color_pallet['menu-foreground'],
            bg=self._color_pallet['menu-background'],
            font=('Arial', 14, 'bold')
        )
        self._labels['mini_menu'].bind('<Button-1>', self._slide_side_bar_in)
        self._frames['sidebar'].bind("<Leave>", self._slide_side_bar_out)
        

    def _slide_side_bar_in(self, event=None):
        print("slide in")
        self._labels['mini_menu'].place_forget()
        
        # I can latter add a smooth effect, but so far it will be enough

    def _slide_side_bar_out(self, event=None):
        # I can latter add a smooth effect, but so far it will be enough
        self._labels['mini_menu'].place(
            relx=0.45, rely=0.01, relwidth=0.1, relheight=0.05
        )

    def _create_bottom_bar(self, links=[]):
        self._frames["footer"] = Tk.Frame(
            self._root, 
            name="footer",
            bg = self._color_pallet["bottom-background"]
        )
        self._frames["footer"].place(
            relx=0, rely=0.95, relheight=0.05, relwidth=1
        )

    def _create_pages(self):
        pass
            

        
