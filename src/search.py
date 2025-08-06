from os import path, getcwd
import logging 
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from time import sleep, time

class Search():
    def __init__(self, browser=None, log=None):
        self._browser = browser
        self._log = log
        self._internal_log = None
        self._log_name = ""

    def _get_browser(self, visible=True):
        if isinstance(self._browser, webdriver.Firefox):
            return self._browser
        options = FirefoxOptions()
        if not visible:
            options.add_argument("-headless")
        self._browser=webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        return self._browser

    def close(self):
        try:
            if isinstance(self._browser, webdriver.Firefox):
                self._browser.quit()
        except Exception as e:
            print("close: failed while trying to close the webdriver")

        
    def _get_logger(self):
        if isinstance(self._log, logging.Logger):
            return self._log
        if isinstance(self._internal_log, logging.Logger):
            return self._internal_log

        self._log_name = path.join(getcwd(), "search_log.log")
        self._internal_log = logging.getLogger("SEARCH")
        logging.basicConfig(filename=self._log_name, level=logging.ERROR)
        return self._internal_log

    def _basic_search(self, code, filter_func, timeout_in_seconds=10):
        browser = self._get_browser()
        log = self._get_logger()
        tries = 150
        sleep_time = timeout_in_seconds / tries
        result = []
        while tries > 0:
            result = []
            try:
                elements = browser.execute_script(code)
                if isinstance(elements, list) and len(elements) > 0:
                    for element in elements:
                        if isinstance(element, webdriver.remote.webelement.WebElement):
                            if filter_func(element):
                                result.append(element)
                    if len(result) > 0:
                        break
                if isinstance(elements, webdriver.remote.webelement.WebElement):
                        if filter_func(elements):
                            result.append(elements)
                            break
            except StaleElementReferenceException as e:
                log.info(f"_basic_search: failed but can continue, {e}, {type(e)} ")
            except Exception as e:
                log.error(f"_basic_search: failed and can't continue, {e}, {type(e)} ")
                raise e
            tries -= 1
            sleep(sleep_time)
        if tries <= 0:
            raise TimeoutError("_basic_search: Failed to find the element")
        return result
    
    def _basic_search_from_parent(self, parent, code, filter_func, timeout_in_seconds=10):
        browser = self._get_browser()
        log = self._get_logger()
        tries = 150
        sleep_time = timeout_in_seconds / tries
        result = []
        while tries > 0:
            result = []
            try:
                elements = browser.execute_script(code, parent)
                if isinstance(elements, list) and len(elements) > 0:
                    for element in elements:
                        if isinstance(element, webdriver.remote.webelement.WebElement):
                            if filter_func(element):
                                result.append(element)
                    if len(result) > 0:
                        break
                if isinstance(elements, webdriver.remote.webelement.WebElement):
                        if filter_func(elements):
                            result.append(elements)
                            break
            except StaleElementReferenceException as e:
                log.info(f"_basic_search_from_parent: failed but can continue, {e}, {type(e)} ")
            except Exception as e:
                log.error(f"_basic_search_from_parent: failed and can't continue, {e}, {type(e)} ")
                raise e
            tries -= 1
            sleep(sleep_time)
        if tries <= 0:
            raise TimeoutError("_basic_search_from_parent: Failed to find the element")
        return result


    def load_page(self):
        browser = self._get_browser()
        log = self._get_logger()
        browser.get("https://www.camara.leg.br/")
        return self._wait_for_page_to_load()
    
    def _wait_for_page_to_load(self):
        target_class = "noticias-home"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : \
            str(element.get_attribute("innerHTML")).strip() != "" and \
            element.tag_name == "div"
        result = self._basic_search(code, filter_func)
        return (len(result) > 0)

    def _click_on_deputies(self):
        log = self._get_logger()
        browser = self._get_browser()
        target_class = "menu-global__item-deputados nav-link dropdown-toggle"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : \
            str(element.get_attribute("innerHTML")).strip() == "Deputados" and \
            element.tag_name == "a"
        result = self._basic_search(code, filter_func)
        if len(result) > 0:
            try:
                #result[0].click()
                browser.execute_script("arguments[0].click();", result[0])
            except StaleElementReferenceException as e:
                log.error(f'_click_on_deputies:failed to click on the element,page still loading')
                raise e
                #should try more times
            except Exception as e:
                print("click failed", e, type(e))
                log.error(f'_click_on_deputies: failed to click on the element, {type(e)}')
                raise e
            else:
                return True
        return False

    def _click_quem_sao_link(self):
        log = self._get_logger()
        browser = self._get_browser()
        target_class = "a"
        code = f"return document.getElementsByTagName('{target_class}');"
        filter_func = lambda element : \
            str(element.get_attribute("innerHTML")).strip() == "Quem são" 
        result = self._basic_search(code, filter_func)
        if len(result) > 0:
            try:
                browser.execute_script("arguments[0].click();", result[0])
            except StaleElementReferenceException as e:
                print("_click_on_deputies: click failed")
                log.error(f'_click_on_deputies:failed to click on the element,page still loading')
                raise e
                #should try more times
            except Exception as e:
                log.error(f'_click_quem_sao_link: failed to reach the quem sao page')
                raise e
            else:
                return True
        return False

    def _wait_for_deputies_search_page_to_load(self):
        target_class = "titulo-landing"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : \
                str(element.get_attribute("innerHTML")).strip().find("Quem são os deputados") >= 0 and \
                element.tag_name == 'h1'
        result = self._basic_search(code, filter_func, timeout_in_seconds=20)
        return (len(result) > 0)

    def _select_mandate(self, mandate=57):
        log = self._get_logger()
        browser = self._get_browser()
        target_class = "form-control busca__campo"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : \
            str(element.get_attribute("name")).strip() == "legislatura" 
        result = self._basic_search(code, filter_func)
        if len(result) > 0:
            try:
                browser.execute_script(f"arguments[0].value='{mandate}';", result[0])
            except StaleElementReferenceException as e:
                print("_select_mandate: click failed")
                log.error(f'_select_mandate:failed to select the mandate')
                raise e
                #should try more times
            except Exception as e:
                log.error(f'_select_mandate: failed to select the mandate {e}, type{e}')
                raise e
            else:
                return True
        return False

    def _click_search_button(self):
        log = self._get_logger()
        browser = self._get_browser()
        target_class = "button button--sm"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : \
            str(element.get_attribute("innerHTML")).strip() == "Buscar" 
        result = self._basic_search(code, filter_func)
        if len(result) > 0:
            try:
                browser.execute_script("arguments[0].click();", result[0])
            except StaleElementReferenceException as e:
                print("_click_search_button: click failed")
                log.error(f'_click_search_button:failed to click on search')
                raise e
                #should try more times
            except Exception as e:
                log.error(f'_click_search_button: failed to click on search{e}, type{e}')
                raise e
            else:
                return True
        return False

    def _wait_for_results_page_to_load(self):
        target_class = "nome-deputado"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : True 
        result = self._basic_search(code, filter_func)
        return (len(result) > 0)

    def _get_deputies_links(self):
        log = self._get_logger()
        target_class = "nome-deputado"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element: element.tag_name == "a"
        tries = 3
        while tries > 0:
            try:
                result = self._basic_search(code, filter_func)
                data = {}
                for representative in result:
                    name = str(representative.get_attribute("innerHTML"))
                    link = str(representative.get_attribute("href"))
                    data[name] = link
            except StaleElementReferenceException as e:
                pass
            except Exception as e:
                log.error(f'_get_deputies_links failed to get the links {e} {type(e)}')
                raise e
            else:
                break
            tries -= 1
            sleep(2)
        return data

    def _is_enabled(self):
        target_class = "pagination-list__nav pagination-list__nav--next"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : True 
        result = self._basic_search(code, filter_func)
        if len(result) != 1:
            return False 
        return (str(result[0].get_attribute("class")).find("disabled") < 0)


    def _change_page(self):
        if not self._is_enabled():
            return False
        log = self._get_logger()
        browser = self._get_browser()
        target_class = "pagination-list__nav-link"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : \
            str(element.get_attribute("innerHTML")).strip().find("Próxima") >= 0
        result = self._basic_search(code, filter_func)
        if len(result) > 0:
            try:
                result[0].click()
                #browser.execute_script("arguments[0].click();", result[0])
            except StaleElementReferenceException as e:
                print("_click_search_button: click failed")
                input("stuck here")
                log.error(f'_click_search_button:failed to click on search')
                raise e
                #should try more times
            except Exception as e:
                log.error(f'_click_search_button: failed to click on search{e}, type{e}')
                raise e
            else:
                return True
        return False

    def _extract_name_party_and_state(self, value):
        start_pos = value.find("(")
        end_pos = value.find(")")
        name = ""
        party = ""
        state = ""
        if end_pos > start_pos and start_pos >= 0:
            party_state = value[start_pos:end_pos]
            pair = party_state.split("-")
            name = value[0:start_pos].strip()
            if len(pair) == 2:
                party = pair[0].replace("(","").replace("(","")
                state = pair[1].replace("(","").replace(")","")
        return name, party, state

    def _wait_for_representative_page_to_load(self):
        target_class = "l-identificacao-landing"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : element.tag_name == 'div'
        result = self._basic_search(code, filter_func)
        return (len(result) > 0)

    def _read_personal_information(self):
        target_class = "informacoes-deputado"
        code = f"return document.getElementsByClassName('{target_class}');"
        filter_func = lambda element : element.tag_name == "ul" 
        blocks = self._basic_search(code, filter_func)
        target_tag = "li"
        code = f"return arguments[0].getElementsByTagName('{target_tag}');"
        filter_fund = lambda element : element.tag_name == "li"
        result = {}
        for block in blocks:
            items = self._basic_search_from_parent(block, code, filter_fund)
            for item in items:
                data = self._clear_html_tags(item.get_attribute("innerHTML"))
                if data.find(":") >= 0:
                    values = data.split(":")
                    key = str(values[0]).replace("\n","").strip()
                    value = str(values[1]).replace("\n","").strip()
                    result[key] = value
        return result

    def _clear_html_tags(self, value):
        start_pos = value.find("<")
        end_pos = value.find(">")
        while start_pos >= 0 and end_pos >= 0:
            start_pos = value.find("<")
            end_pos = value.find(">")
            tag = value[start_pos:end_pos+1]
            value = value.replace(tag, "", 1)
        return value.strip()

    def _extract_data_from_representative_page(self, link):
        browser = self._get_browser()
        browser.get(link)
        self._wait_for_representative_page_to_load()
        return self._read_personal_information()


    def access_deputies_page(self):
        self.load_page()
        self._click_on_deputies()
        self._click_quem_sao_link()
        self._wait_for_deputies_search_page_to_load()
        self._select_mandate()
        self._click_search_button()
        self._wait_for_results_page_to_load()
        return True
   
    def get_all_links(self):
        count = 0
        max_tries = 100
        all_data = {}
        while max_tries > 0:
            data = self._get_deputies_links()
            for key,value in data.items():
                all_data[key] = value
            result = self._change_page()
            self._wait_for_results_page_to_load()
            count += 1
            max_tries -= 1
            if not result:
                break
        return all_data 

    def get_representative_data(self, representative, link):
        name, party, state = self._extract_name_party_and_state(representative)        
        result = self._extract_data_from_representative_page(link)
        if isinstance(result, dict):
            result["Nome"] = name
            result["Estado"] = state
            result["Partido"] = party
        result["Status"] = "ativo"
        if result.get("E-mail", "") == "":
            result["Status"] = "inativo"
        return result 





            


