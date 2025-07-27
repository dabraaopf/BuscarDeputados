from src.interface import GUI
from tkinter import Tk
from tkinter import ttk
from os import path, getcwd
from src.search import Search
from src.storage import Storage
import threading 

class Main(GUI):
    def __init__(self, root):
        self._config_path = path.join(getcwd(),"var","config.json")
        super().__init__(root, self._config_path)
        self._set_actions()
        
    def _set_actions(self):
        self._pages["main"].bind_event("button", "search", "<Button-1>", self._run)

    def _run(self, event=None):
        print("should run")

if __name__ == "__main__":
    root = Tk()
    window = Main(root)
    root.mainloop()
