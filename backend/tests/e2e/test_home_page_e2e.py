import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
import time

class TestCart():
    def setup_method(self):
        service=ChromeService(ChromeDriverManager().install())
        self.driver=webdriver.Chrome()
        #driver=webdriver.Edge()

        self.driver.get("http://localhost:8000")
        self.driver.maximize_window()
        time.sleep(2)

    def teardown_method(self):
        self.driver.quit()

    def test_scroll(self):
        self.driver.execute_script("window.scrollTo(0,300)")
        time.sleep(5)
