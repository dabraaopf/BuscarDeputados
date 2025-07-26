from src.interface import GUI
from tkinter import Tk
from tkinter import ttk
from os import path, getcwd

class Main(GUI):
    def __init__(self, root):
        self._config_path = path.join(getcwd(),"var","config.json")
        super().__init__(root, self._config_path)
        
    def _set_actions(self):
        pass

if __name__ == "__main__":
    root = Tk()
    window = Main(root)
    root.mainloop()
