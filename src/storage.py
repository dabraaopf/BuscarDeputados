from os import path, getcwd
import logging 
import sqlite3
from enum import IntEnum, auto

class PolicitianStatus(IntEnum):
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

    def close(self):
        print(type(self._connection))
        try:
            self._connection.close()
        except Exception as e:
            print("failed while trying to close the connection", type(e), e)
            self._connection = None
        return

    def _create_tables():
        log = self._get_logger()
        self._connection = sqlite3.connect(self._storage_path)
        sql = """CREATE TABLE IF NOT EXISTS Politicians(
            id INT PRIMARY KEY,
            name varchar(150) NOT NULL,
            email varchar(250) UNIQUE,
            party varchar(5),
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

    def disable_all_out_of_mandate(self, politicians):
        log = self._get_logger()
        query = f"""SELECT id,name,party FROM Politicians WHERE status = {PolicitianStatus.ACTIVE}"""
        connection = self._get_connection()
        cursor = connection.cursor()
        list_to_disable = []
        try:
            cursor.execute(query)
        except Exception as e:
            log.error(f'disable_all_out_of_mandate: failed to get all policitans, {type(e)}, {e}')
            raise e
        else:
            NAME = 1
            ID = 0
            PARTY = 2
            for record in cursor.fetchall():
                if not record[NAME] in policitians.keys() or politicians[record[NAME]] != record[PARTY]:
                    list_to_disable.append((record[ID]))
        if len(list_do_disable) == 0:
            return
        query = f"""UPDATE Policitans SET status={PolicitanStatus.NO_MANDATE} WHERE id=?"""
        try:
            cursos.executemany(query,list_to_disable)
        except Exception as e:
            log.error(f'disable_all_out_of_mandate: failed to update the representatives not in mandate anymore {type(e)} {e}')
            raise e
        else:
            return True

    def add_politicians(self, politicians={}):
        lines = []
        for key, value in politicians.items():                
            lines.append(
                (
                    politicians[key].get("name",""),
                    politicians[key].get("email", ""),
                    politicians[key].get("party", ""),
                    politicians[key].get("state", ""),
                    politicians[key].get("start_mandate",0), 
                    politicians[key].get("end_mandate",0),
                    politicians[key].get("status", PoliticianStatus.INACTIVE)
                )
            )
        query = """INSERT INTO Politicians 
        (name, email, party, state, start_mandate, end_mandate, status) 
        VALUES 
        ('?', '?', '?', '?', ?, ?, ?)"""
        log = self._get_logger()
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.executemany(query, lines)
        except Exception as e:
            log.error(f'add_politicians: failed to add a new politician {type(e)} {e}')
            raise e
        else:
            cursor.commit()
        return True

    def add_search_status(self, status):
        query = f"""INSERT INTO Searchs(lastUpdate, status) VALUES
        ({lastUpdate}, {status})"""
        log = self._get_logger()
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.executemany(query)
        except Exception as e:
            log.error(f'add_search_status: failed to save the search status {type(e)} {e}')
            raise e
        else:
            cursor.commit()
        return True



