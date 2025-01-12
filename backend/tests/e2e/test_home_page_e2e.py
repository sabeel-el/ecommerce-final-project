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
import re
import random
import string

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class TestShop():
    def setup_method(self):
        service=ChromeService(ChromeDriverManager().install())
        self.driver=webdriver.Chrome()
        #driver=webdriver.Edge()
        self.driver.get("http://localhost:8000")
        self.driver.maximize_window()
        time.sleep(2)

    def teardown_method(self):
        self.driver.quit()

    def login(self):
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("cusomer@mail")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("customer")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        time.sleep(3)
   

    def test_scroll(self):
        self.driver.execute_script("window.scrollTo(0,300)")
        time.sleep(5)

    def test_search(self):
        self.driver.find_element(By.NAME, "q").click()
        self.driver.find_element(By.NAME, "q").send_keys("totebag")
        self.driver.find_element(By.CSS_SELECTOR, ".p-2").click()
        WebDriverWait(self.driver, 30).until(expected_conditions.url_changes("http://localhost:8000"))
        products_title = self.driver.find_elements(By.CSS_SELECTOR, ".card-body .card-title strong")
        for product in products_title:
            product_name = product.text.lower()  
            assert 'totebag' in product_name

    def test_register(self):
        random_suffix = generate_random_string()
        name = f"TESTUSER{random_suffix}"
        email = f"{name.lower()}@example.com"  
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        self.driver.find_element(By.ID, "name").click()
        self.driver.find_element(By.ID, "name").send_keys(name)
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("name")
        self.driver.find_element(By.ID, "passwordConfirm").click()
        self.driver.find_element(By.ID, "passwordConfirm").send_keys("name")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        WebDriverWait(self.driver,30).until(expected_conditions.presence_of_element_located((By.ID,"username")))
        user_name=self.driver.find_element(By.ID, "username")
        assert user_name.text==name

    def test_logout_login(self):
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("cusomer@mail")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("customer")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        time.sleep(2)
        assert self.driver.find_element(By.ID, "username").text=="CUSTOMER"
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
  
    def test_place_order(self):
        self.login()
        WebDriverWait(self.driver,15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,".col-xl-3:nth-child(4) strong")))
        self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(4) strong").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".w-100").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".w-100").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "address").click()
        self.driver.find_element(By.ID, "address").send_keys("athar")
        self.driver.find_element(By.ID, "city").click()
        self.driver.find_element(By.ID, "city").send_keys("rahat")
        self.driver.find_element(By.ID, "postalCode").click()
        self.driver.find_element(By.ID, "postalCode").send_keys("1234")
        self.driver.find_element(By.ID, "country").click()
        self.driver.find_element(By.ID, "country").send_keys("Israel")
        self.driver.find_element(By.CSS_SELECTOR, ".my-3").click()
        self.driver.find_element(By.CSS_SELECTOR, ".my-3").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, ".w-100").click()
        time.sleep(3)
        order=self.driver.find_element(By.CSS_SELECTOR, "h1").text
        match = re.search(r'ORDER:\s*(\d+)', order)
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.LINK_TEXT, "Profile").click()
        # element = self.driver.find_element(By.LINK_TEXT, "Profile")
        # actions = ActionChains(self.driver)
        # actions.move_to_element(element).perform()
        table = WebDriverWait(self.driver, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".table-responsive")))
        # Find all <td> elements inside the table
        order_cells = table.find_elements(By.TAG_NAME, "td")
        # Check if the desired order number is present
        order_number =match.group(1)
        print(order_number)
        assert any(order_number == cell.text for cell in order_cells)    
