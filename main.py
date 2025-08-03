from src.interface import GUI
from tkinter import Tk
from tkinter import ttk
from tkinter import *
from os import path, getcwd
rom src.search import Search
from src.storage import Storage
import threading 

class Main(GUI):
    def __init__(self, root):
        self._config_path = path.join(getcwd(),"var","config.json")
        super().__init__(root, self._config_path)
        self._set_actions()
        self._load_page(name="main")
        
    def _set_actions(self):
        self._pages["main"].bind_event("button", "search", "<Button-1>", self._run)
        self._side_menu_options['details'].bind("<Button-1>", self._fill_details)
        self._side_menu_options['log'].bind("<Button-1>", self._fill_logs)

    def _fill_details(self, event=None):
        self._pages['details']._entries_values['author'].set(
            self._configs.get("author", "failed")
        )
        self._pages['details']._entries_values['name'].set(
            self._configs.get("name", "failed")
        )
        self._pages['details']._entries_values['version'].set(
            self._configs.get("version", "failed")
        )
        self._pages['details']._entries_values['description'].set(
            self._configs.get("description", "failed")
        )
        self._load_page(event)

    def _fill_logs(self, event=None):
        try:
            with open(self._log_path, 'r') as fl:
                data = fl.read()
        except Exception as e:
            log = self._get_logger()
            log.error(f'_fill_logs: failed to open the log file {type(e)} {e}')
        else:
            self._pages['log']._entries['logs'].insert(END,data)
        finally:
            self._load_page(event)

    def _run(self, event=None):
        print("should run")

if __name__ == "__main__":
    root = Tk()
    window = Main(root)
    root.mainloop()
