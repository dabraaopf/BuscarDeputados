import importlib
import test_search 
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from time import sleep, time


def get_browser(visible=True):
    options = FirefoxOptions()
    if not visible:
        options.add_argument("-headless")
    browser=webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    return browser

def reload(browser):
    importlib.reload(test_search)
    from test_search import TestSuit
    return TestSuit(browser)

if __name__ == "__main__":
    answer = ""
    browser = None
    test_list = []
    while answer != "x":
        answer = input("Please inform what tests do you want to run (h-help, x-quit): ").lower()
        if answer == "h": 
            test = reload(browser)
            print(test)
        elif answer != "x":
            if not isinstance(browser, webdriver.Firefox):
                browser = get_browser()
            test = reload(browser)

            if answer == "" and test_list != []:
                test.run(test_list)
            elif answer.find(",") < 0:
                test_list = [answer]
                test.run(test_list)
            elif answer.find(",") > 0:
                test_list = answer.split(",")
                test.run(test_list)

    if isinstance(browser, webdriver.Firefox):
        try:
            browser.quit()
        except Exception as e:
            print(f"Failed to kill the browser, {type(e)}, {e}, {traceback.print_exc()}")
        else:
            print("Eveything clean")
        finally:
            browser = None






            
