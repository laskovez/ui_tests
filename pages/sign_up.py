from pages import BasePage
from pages.login import LoginLocators as login_loc


class SignUpPage(BasePage):

    def fill_sign_up_form(self, first_name: str = None, last_name: str = None,
                          login: str = '', password: str = None):
        if first_name:
            self.send_keys(first_name, sign_up_loc.FIRST_NAME)
        if last_name:
            self.send_keys(last_name, sign_up_loc.LAST_NAME)
        if login:
            self.send_keys(login, login_loc.EMAIL_INPUT)
        if password:
            self.send_keys(password, login_loc.PASS_INPUT)

    def confirm_policy(self):
        self.click(sign_up_loc.POLICY_CONFIRM)

    def enter_confirm_code(self, code: str):
        self.send_keys(code, sign_up_loc.CONFIRM_CODE)

    def open_sign_up_page(self):
        self.visit('/login')
        self.should_be_sign_up_page()

    def should_be_sign_up_page(self):
        self.should_be_sign_up_url()
        self.should_be_sign_up_form()

    def should_be_sign_up_url(self):
        assert 'login' == self.current_url.split('/')[-1], 'Opened page is not sign up page'

    def should_be_sign_up_form(self):
        self.check_element_is_visible(sign_up_loc.REGISTER_FORM)

    def click_sign_up(self):
        self.click(sign_up_loc.SIGN_UP_BTN)


class SignUpLocators:
    REGISTER_FORM = '//div[@data-id="registration-form"]'
    POLICY_CONFIRM = '//mat-checkbox[@data-id="policy_confirm"]'
    SIGN_UP_BTN = '//button[@data-id="sign-up-btn"]'
    FIRST_NAME = '//input[@data-id="first_name"]'
    LAST_NAME = '//input[@data-id="last_name"]'
    CONFIRM_CODE = '//input[@data-id="confirm-code-input"]'


sign_up_loc = SignUpLocators
