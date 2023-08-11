import time
import logging
logger = logging.getLogger(__name__)

from copy import deepcopy
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService

class SeleniumEmulator:
    def __init__(self, chrome_portable_exe_path=None, headless=True, **kwargs):
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless=new')
        if chrome_portable_exe_path:
            chrome_options.binary_location = chrome_portable_exe_path

        chrome_options.add_experimental_option(
            "prefs", {
                "download.default_directory": "/dev/null", 
                "download.prompt_for_download": False, 
            }
        )
        self.driver = Chrome(options = chrome_options)
        self.actions = ActionChains(self.driver)
        self.driver.implicitly_wait(5.0)
        self.driver.set_page_load_timeout(10.0)
        self.INIT_SCRIPT = open("./src/default.js", 'r').read()

    def quit(self, ):
        self.driver.quit()

    def find_element(self, by:callable, value:str):
        try:
            # element =  WebDriverWait(self.driver, waiting_time).until(EC.visibility_of_element_located((by, value)))
            element =  self.driver.find_element(by, value)
            return element
        except:
            return None
    
    def open_new_tab(self):
        self.driver.switch_to.new_window('tab')

    def goto_url(self, url:str, delay:float=1.0):
        self.driver.get(url)
        time.sleep(delay)

    def get_current_url(self):
        return self.driver.current_url
        