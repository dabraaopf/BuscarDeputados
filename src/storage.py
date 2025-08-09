from os import path, getcwd
import logging 
import sqlite3
from enums import Enum, auto

class PolicitianStatus(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    NO_MANDATE = auto()

class Storage():
    def __init__(self, storage_path="", log=None):
        self._storage_path = storage_path 
        self._connection = None
        self._cursor = None
        self._log = log
        self._internal_log = None
        self._log_name = ""

    def _get_connection(self):
        if not path.exists(self._storage_path):
            self._create_tables()
        if isinstance(self._connection, sqlite.Connection):
            return self._connection
        self._connection = sqlite3.connect(self._storage_path)
        return self._connection

    def _create_tables():
        log = self._get_logger()
        self._connection = sqlite3.connect(self._storage_path)
        sql = """CREATE TABLE IF NOT EXISTS Politicians(
            id INT PRIMARY KEY,
            name varchar(150) NOT NULL,
            email varchar(250) UNIQUE,
            state varchar(2) NOT NULL,
            start_mandate INT,
            end_mandate INT,
            status INT 
        )
        """
        cursor = self._connection.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            log.error(f'_create_tables: failed to create the table {e} {type(e)}') 
            raise e
        else:
            sql = """CREATE TABLE IF NOT EXISTS Searchs(
                lastUpdate INT, 
                status varchar(1)
            )
            """
            cursor.execute(sql)
            return True
        return False
        
    def _get_logger(self):
        if isinstance(self._log, logging.Logger):
            return self._log
        if isinstance(self._internal_log, logging.Logger):
            return self._internal_log

        self._log_name = path.join(getcwd(), "storage_log.log")
        self._internal_log = logging.getLogger("STORAGE")
        loggin.basicConfig(filename=self._log_name, level=logging.ERROR)
        return self._internal_log

    def add_politician(self, politician):
        
        pass

    def add_search_status(self, status):
        pass


