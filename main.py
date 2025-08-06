from src.interface import GUI
from tkinter import Tk
from tkinter import ttk
from tkinter import *
from os import path, getcwd
from src.search import Search
from src.storage import Storage
from threading import Thread
import traceback
import pdb

class Main(GUI):
    def __init__(self, root):
        self._config_path = path.join(getcwd(),"var","config.json")
        super().__init__(root, self._config_path)
        self._set_actions()
        self._load_page(name="main")
        self._thread = None
        
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
        if isinstance(self._thread, Thread) and self._thread.is_alive():
            self._entries_values["short-text"].set("Processo ainda em execução")
            return
        self._thread = Thread(target=self._get_representatives_data, args=[], daemon=True)
        self._thread.start()

    def _get_representatives_data(self):
        log = self._get_logger()
        search = Search(log=log)
        self._entries_values["short-text"].set("Processo iniciando")
        try:
            search.access_deputies_page()
            self._entries_values["short-text"].set("Site carregado com sucesso, buscando deputados")
            representatives = search.get_all_links()
            self._entries_values["short-text"].set(f"Páginas carregadas, {len(representatives.keys())} deputados encontrados")
            target_keys = ["Nome", "Partido", "Estado", "E-mail", "Status"]
            self._set_heaers_to_listview(target_keys)
            total = len(representatives.keys())
            i = 0
            perc = 0
            previous_perc = 1
            # TODO
            #add persistency
            #add statistics with pandas + numpy
            for name, link in representatives.items():
                row = search.get_representative_data(name, link)
                self._populate_list_view(row, target_keys, i+1)
                i+=1
                perc = int(i/total*100)
                if perc != previous_perc:
                    self._entries_values["short-text"].set(f"Buscando dados ( {perc}% )")
                    previous_perc = perc
        except Exception as e:
            self._entries_values["short-text"].set("Processo falhou, veja os logs para obter mais detalhes")
            log.error(f'_get_representatives_data: failed to get the deputies data {e} {type(e)} {traceback.print_exc()}')
        else:
            self._entries_values["short-text"].set(f"Processo finalizado")
        
    def _populate_list_view(self, row, target_keys, index):
        values = []
        for key in target_keys:
            values.append(row.get(key, "-"))
        self._pages["main"]._entries["representatives"].insert(
            '',
            'end',
            text=f"{index}",
            values=values
        )

    def _set_heaers_to_listview(self, target_keys):
        for index, column_text in enumerate(target_keys):
            self._pages["main"]._entries["representatives"].heading(column=f"col{index}", text=column_text)

if __name__ == "__main__":
    root = Tk()
    window = Main(root)
    root.mainloop()
