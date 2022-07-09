from pages import BasePage


class BaseTest:

    page = None

    @classmethod
    def setup_class(cls):
        cls.page = BasePage()

    @classmethod
    def teardown_class(cls):
        cls.page.browser.close()
