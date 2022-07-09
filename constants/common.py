from constants import Enum


class BrowserName(Enum):
    CHROME = 'chrome'


class BrowserType(Enum):
    CHROME_NATIVE = "Chrome Native"
    CHROME_HEADLESS = "Chrome Headless"


class Gmail(Enum):
    EMAIL_TO = 'testmonitoringqa@gmail.com'
    DEFAULT_LABEL_ID = 'INBOX'
    EMAIL_FROM_FILTER = 'support@eos.com'
    EMAIL_AWAIT_TIME_SECONDS = 60
