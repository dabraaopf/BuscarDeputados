from os import path, getcwd
import logging 
import sqlite3

class Storage():
    def __init__(self, stora_path="", log=None):
        self._storage_path = stora_path 
        self._connection = None
        self._cursor = None
        self._log = log
        self._internal_log = None
        self._log_name = ""

    def _get_connection(self):
        if isinstance(self._connection, sqlite.Connection):
            return self._connection
        
    def _get_logger(self):
        if isinstance(self._log, logging.Logger):
            return self._log
        if isinstance(self._internal_log, logging.Logger):
            return self._internal_log

        self._log_name = path.join(getcwd(), "storage_log.log")
        self._internal_log = logging.getLogger("STORAGE")
        loggin.basicConfig(filename=self._log_name, level=logging.ERROR)
        return self._internal_log

