from pages.login import LoginPage
from tests import BaseTest


class TestLogin(BaseTest):
    login = LoginPage()

    def test001_login_with_valid_credentials(self):
        self.login.open_login_page()
        self.login.fill_login_form()
        self.login.click_sign_in()
        self.login.check_user_authenticated()
