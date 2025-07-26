from os import path, getcwd
import logging 

class Search():
    def __init__(self, browser=None, log=None):
        self._browser = browser
        self._log = log
        self._internal_log = None
        self._log_name = ""

    def _get_browser(self):
        if isinstance(self._browser, webdriver.Firefox):
            return self._browser
        
    def _get_logger(self):
        if isinstance(self._log, logging.Logger):
            return self._log
        if isinstance(self._internal_log, logging.Logger):
            return self._internal_log

        self._log_name = path.join(getcwd(), "search_log.log")
        self._internal_log = logging.getLogger("SEARCH")
        loggin.basicConfig(filename=self._log_name, level=logging.ERROR)
        return self._internal_log

