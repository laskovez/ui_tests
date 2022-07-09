import os

from dotenv import load_dotenv

from constants import Enum

load_dotenv()
env = os.getenv('TESTS_ENV')


class Environment(Enum):
    TEST_ORG = os.getenv('TEST_ORG')
    DEFAULT_USER_SA = os.getenv('DEFAULT_USER_SA')
    DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD')

    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'
    TEST = 'test'

    if env == PRODUCTION:
        BASE_URL = 'https://crop-monitoring.eos.com/'
        FREE_USER_EMAIL = 'testmonitoringqa@gmail.com'
        FREE_USER_PASS = '11111111'

