import re
import time

from pages.login import LoginPage
from pages.sign_up import SignUpPage
from tests import BaseTest
from utils.gmail_api.gmail_api_emails import SendMail
from utils.utils import get_new_random_email_from_default


class TestSignUp(BaseTest):
    login = LoginPage()
    sign_up = SignUpPage()
    emails = SendMail()

    def test001_sign_up_with_valid_data(self):
        email = get_new_random_email_from_default()
        self.sign_up.open_sign_up_page()
        self.sign_up.confirm_policy()
        self.sign_up.fill_sign_up_form('test', 'test', email, '11111111')

        # wait until "/validate" request will be finished, don't have time for more elegant decision.
        # It is actually a bug. "Sign up" button click should follow
        # some action even if we wait for "/validate" response.
        # For now, only when the "/validate" request is finished, "Sign up" button click does anything
        time.sleep(3)

        self.sign_up.click_sign_up()

        email = self.emails.wait_and_read_message(contains=email, await_time_seconds=15)
        confirm_code = re.findall(r'10px 20px;text-align: center;">(.*)<', str(email['msg_body']))[0]
        self.sign_up.enter_confirm_code(confirm_code)
        self.login.check_user_authenticated()
