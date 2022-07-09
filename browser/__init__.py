from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config
from constants.common import BrowserType
from constants.environmets import Environment
from utils.utils import get_driver_path


class Browser(object):
    driver = None
    browser = config.BROWSER
    timeout = 10

    @classmethod
    def __init__(cls):
        if not cls.driver:
            options = Options()
            capabilities = DesiredCapabilities.CHROME.copy()
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--lang=en')

            if config.BROWSER_TYPE == BrowserType.CHROME_HEADLESS:
                options.add_argument("--headless")
                print("Calling headless local config")
                cls.driver = webdriver.Chrome(get_driver_path(cls.browser), options=options,
                                              desired_capabilities=capabilities)
            else:
                print("starting default webdriver config")
                cls.driver = webdriver.Chrome(get_driver_path(cls.browser), desired_capabilities=capabilities,
                                              options=options)
            cls.driver.delete_all_cookies()
            cls.driver.implicitly_wait(0.5)
            cls.driver.set_window_size(1800, 900)
            print("Starting browser using capabilities:\n", cls.driver.desired_capabilities)

    # BROWSER

    def visit(self, url=''):
        self.driver.get(Environment.BASE_URL + url)

    # GET AND CLICK

    def find(self, loc, wait=None):
        try:
            return self.wait_for_element_presence(loc, timeout=wait if wait is not None else self.timeout)
        except Exception:
            message = f"Element not found by: {loc,} in {self.timeout} seconds"
            raise TimeoutException(msg=f'\n{message}\n')

    def find_elements(self, loc):
        return self.driver.find_elements_by_xpath(loc)

    def scroll_into_element_view(self, element=None, element_locator: str = None):
        if element_locator:
            element = self.find(element_locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def move_to_element(self, element=None, element_locator=None, attempt_number=1):
        if element_locator:
            element = self.find(element_locator)
        try:
            (ActionChains(self.driver)
             .move_to_element(element)
             .perform())

        except MoveTargetOutOfBoundsException as e:
            if attempt_number > 2:
                raise e

            self.scroll_into_element_view(element=element, element_locator=element_locator)
            self.move_to_element(element=element, element_locator=element_locator, attempt_number=(attempt_number + 1))

    def click(self, element_locator=None):
        self.wait_for_element_visible(element_locator=element_locator)
        self.move_to_element(element_locator=element_locator)
        self.wait_for_element_to_be_clickable(element_locator).click()

    # SET VALUE

    def send_keys(self, keys, loc):
        self.find(loc).send_keys(keys)

    # CLEAR VALUE

    @staticmethod
    def clear_field_with_keys(input_web_element):
        input_web_element.send_keys(Keys.CONTROL + "a" + Keys.DELETE + Keys.BACKSPACE)

    # WAITS

    def wait_for_element_to_be_clickable(self, element_locator, timeout=None):
        return WebDriverWait(self.driver, (self.timeout if not timeout else timeout)).until(
            EC.element_to_be_clickable((By.XPATH, element_locator)))

    def wait_for_element_visible(self, element=None, element_locator: str = None, timeout=None):
        try:
            if element_locator:
                element = WebDriverWait(self.driver, (self.timeout if not timeout else timeout)).until(
                    EC.visibility_of_element_located((By.XPATH, element_locator)))
            else:
                element = WebDriverWait(self.driver, (self.timeout if not timeout else timeout)).until(
                    EC.visibility_of(element))
            return element
        except Exception:
            message = f"Element: {element_locator,} not visible during {self.timeout} seconds"
            raise TimeoutException(msg=f'\n{message}\n')

    def wait_for_element_presence(self, element_locator, timeout=None):
        element = WebDriverWait(self.driver, (self.timeout if not timeout else timeout)).until(
            EC.presence_of_element_located((By.XPATH, element_locator)))
        return element

    def wait_for_element_disappear(self, element_locator, timeout=None):
        try:
            WebDriverWait(self.driver, (self.timeout if not timeout else timeout)).until(
                EC.invisibility_of_element_located((By.XPATH, element_locator)))
        except TimeoutException:
            message = f"Element: {element_locator,} is still visible after {self.timeout} seconds"
            raise TimeoutException(msg=f'\n{message}\n')

    # GET VALUES STORED IN LS, SS

    def get_local_storage_value(self, key):
        return self.driver.execute_script(f"return window.localStorage.getItem('{key}')")

    @property
    def current_url(self):
        return self.driver.current_url

    @classmethod
    def close(cls):
        if cls.driver:
            cls.driver.quit()
            cls.driver = None
