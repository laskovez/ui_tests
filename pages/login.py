import time

from constants.environmets import Environment
from pages import BasePage


class LoginPage(BasePage):

    def fill_login_form(self, login: str = Environment.FREE_USER_EMAIL, password: str = Environment.FREE_USER_PASS):
        if login:
            self.send_keys(login, login_loc.EMAIL_INPUT)
        if password:
            self.send_keys(password, login_loc.PASS_INPUT)

    def open_login_page(self):
        self.visit('/login/auth')
        self.should_be_login_page()

    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()

    def should_be_login_url(self):
        assert '/login/auth' in self.current_url, 'Opened page is not login page'

    def should_be_login_form(self):
        self.check_element_is_visible(login_loc.LOGIN_FORM)

    def click_sign_in(self):
        self.click(login_loc.SIGN_IN_BTN)

    def check_user_authenticated(self):
        # check some content from the home page is shown, to check the home page was opened
        self.check_element_is_visible(login_loc.SEARCH_FIELD)
        assert self.browser.get_local_storage_value('token'), 'No token was set after sig up'
        assert '/main-map/fields/all' in self.current_url, 'The opened page is not home page'


class LoginLocators:
    EMAIL_INPUT = "//input[@data-id='email']"
    PASS_INPUT = '//input[@data-id="password"]'
    LOGIN_FORM = '//div[@data-id="login-form"]'
    SIGN_IN_BTN = '//button[@data-id="sign-in-btn"]'
    SEARCH_FIELD = '//input[@data-id="location-search-input"]'


login_loc = LoginLocators
