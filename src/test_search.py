import importlib
import search 
from time import time, sleep
import traceback
import pdb

class TestSuit():
    def __init__(self, browser=None):
        self._browser = browser
        self._search = None
        self._routines = {
            "test_access_page" : self._test_access_page,
            "test_access_deputies_page" : self._test_access_deputies_page,
            "test_get_representatives_links": self._test_get_representatives_links,
            "test_paginate_thru": self._test_paginate_thru,
            "test_get_all_links": self._test_get_all_links,
            "test_get_information_from_representative_profile":self._test_get_information_from_representative_profile
        }

    def run(self, battery=[]):
        if not isinstance(battery, list):
            return
        if battery == []:
            battery = self._routines.keys()
        for test in battery:
            if test in self._routines.keys():
                start = time()
                try:
                    if self._routines[test]():
                        print(f"[OK] {test} - Time: {time() - start}s")
                    else:
                        print(f"[NOK] {test} - Time: {time() - start}s")
                except AssertionError as e:
                        print(f"[NOK] {test} - Time: {time() - start}s \n {e}")
                except Exception as e:
                        print(f"""[ERROR] {test} - Time: {time() - start}s
                              Type: {type(e)}
                              Traceback: {traceback.print_exc()}""")
    def __str__(self):
        return f"""
            Suit of tests for the Search class

            Tests available: {list(self._routines.keys())}

            To run, call the method "run" and inform (as a list) the test
            routines you want to run, if an empty list is given, it will run
            all tests available
        """

    def _reload(self):
        importlib.reload(search)
        from search import Search
        self._search = Search(browser=self._browser)
        return True

    def _test_access_page(self):
        if not isinstance(self._search, search.Search):
            self._reload()
        assert self._search.load_page(), f"Failed to load the main page"
        return True

    def _test_access_deputies_page(self):
        if not isinstance(self._search, search.Search):
            self._reload()
        assert self._search.load_page(), f"Failed to load the main page"
        assert self._search._click_on_deputies(), f"Failed to click on the deputies link"
        assert self._search._click_quem_sao_link(), f"Failed to click on the quem sao link"
        assert self._search._wait_for_deputies_search_page_to_load(), f"Failed to wait for the filter page to load"
        assert self._search._select_mandate(), f"Failed to select the mandate"
        assert self._search._click_search_button(), f"Failed to click on the search"
        assert self._search._wait_for_results_page_to_load(), f"Failed to load the resuls"
        assert self._browser.page_source.find("Brunini") > 0, f'Failed, no results found'
        return True

    def _test_get_representatives_links(self):
        if not isinstance(self._search, search.Search):
            self._reload()

        assert self._test_access_deputies_page(), f'_test_get_representatives_links: failed to acccess the deputies list'
        data = self._search._get_deputies_links()
        assert  isinstance(data, dict) and data != {}, f'_test_get_representatives_links: failed to get the list of representatives'
        return True

    def _test_paginate_thru(self):
        if not isinstance(self._search, search.Search):
            self._reload()

        assert self._test_access_deputies_page(), f'_test_paginate_thru: failed to acccess the deputies list'
        count = 0
        max_tries = 100
        while max_tries > 0:
            result = self._search._change_page()
            assert result or count > 0, f'_test_paginate_thru: failed to get the list of representatives'
            assert self._search._wait_for_results_page_to_load(), f"_test_paginate_thru: Failed to load the resuls"
            count += 1
            max_tries -= 1
            if not result:
                break
        assert count > 1, f'_test_paginate_thru: too few pages found'
        return True
    
    def _test_get_all_links(self):
        if not isinstance(self._search, search.Search):
            self._reload()
        assert self._test_access_deputies_page(), f'_test_get_all_results: failed to acccess the deputies list'
        count = 0
        max_tries = 100
        all_data = {}
        while max_tries > 0:
            data = self._search._get_deputies_links()
            assert isinstance(data, dict) and data != {}, f"_test_get_all_results: failed to extract any results from the page"
            for key,value in data.items():
                assert not key in all_data.keys(), f'_test_get_all_results: looks like you are reading the same page'
                all_data[key] = value
            result = self._search._change_page()
            assert result or count > 0, f'_test_get_all_results: failed to get the list of representatives'
            assert self._search._wait_for_results_page_to_load(), f"_test_get_all_results: Failed to load the resuls"
            count += 1
            max_tries -= 1
            if not result:
                break
        print(all_data)
        assert count > 1, f'_test_get_all_results: too few pages found'
        return True

    def _test_get_information_from_representative_profile(self):
        if not isinstance(self._search, search.Search):
            self._reload()
        assert self._test_access_deputies_page(), f'_test_get_information_from_representative_profile: failed to acccess the deputies list'
        count = 0
        max_tries = 100
        all_data = {}
        data = self._search._get_deputies_links()
        assert isinstance(data, dict) and data != {}, f"_test_get_information_from_representative_profile: failed to extract any results from the page"
        for key, link in data.items():
            party = self._search._extract_party_and_state(key)
            print("Partido: ", party.get("partido",""), " - Estado: ", party.get("estado", ""))
            self._search._extract_data_from_representative_page(link)
        return True




