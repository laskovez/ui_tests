import os
from random import randint
from sys import platform

from constants.common import Gmail


def set_filepath(filename, directory='', *args):
    """Returns a path to the file in the directories independently of where the func is called from;
     supports any OS;
     usage: filename.txt, -> directory name inside the root dir, -> any directories one by one hierarchically
     to rich filename.txt, separated with comma"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_location = os.path.join(dir_path, os.path.pardir, directory, *args, filename)
    canonical_path = os.path.realpath(file_location)
    return canonical_path


def get_new_random_email_from_default():
    email = Gmail.EMAIL_TO
    return f"{email.split('@')[0]}+{str(randint(1, 100000000))}@gmail.com"


def get_driver_path(drivername):
    """@drivernames: string : chrome, gecko, edge"""
    if platform == 'win32':
        if drivername == 'chrome':
            return set_filepath('chromedriver.exe', r'browser/drivers')
        if drivername == 'gecko':
            return set_filepath('geckodriver.exe', r'browser/drivers')
        if drivername == 'edge':
            return set_filepath('MicrosoftWebDriver.exe', r'browser/drivers')
        else:
            print('Wrong driver name. Possible names: chrome, gecko, edge')
    elif platform == 'linux':
        if drivername == 'chrome':
            # in case of permission error: cd to directory with the driver and use sudo chmod a+x chromedriver
            return set_filepath('chromedriver', r'browser/drivers')
        if drivername == 'gecko':
            return set_filepath(r'browser/drivers')
    else:
        return set_filepath('chromedriver', r'browser/drivers')
