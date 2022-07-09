from selenium.common.exceptions import *

from constants.environmets import Environment
from browser import Browser


class BasePage(object):
    """All page objects inherit from this"""

    def __init__(self):
        self.browser = Browser()
        self.site_url = Environment.BASE_URL

    def visit(self, url=''):
        self.browser.visit(url)

    def click(self, element_locator: str):
        self.browser.click(element_locator)

    def find(self, loc: str, wait=None):
        return self.browser.find(loc, wait=wait)

    def send_keys(self, keys, loc: str):
        self.browser.send_keys(keys, loc)

    def clear_field_with_keys(self, input_web_element):
        self.browser.clear_field_with_keys(input_web_element)

    def check_element_is_visible(self, locator: str, label='element'):
        try:
            self.find(locator)
        except TimeoutException as no_element:
            raise AssertionError(f'"{label}" was not found', no_element.msg)

    def check_element_disappear(self, element_locator, timeout=None):
        try:
            self.browser.wait_for_element_disappear(element_locator, timeout)
        except TimeoutException:
            return False

    @property
    def current_url(self):
        return self.browser.current_url
