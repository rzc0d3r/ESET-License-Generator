# Version: 1.0.8.3 (101023-0017)
VERSION = 'v1.0.8.3 (101023-0017) by rzc0d3r'
import eset_intercepter

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from string import ascii_letters
from random import choice

from modules.shared_tools import *

import os

GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'
DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1

def CreateEmailAndPassword():
    email_obj = eset_intercepter.Email()
    email_obj.register()
    email = email_obj.get_full_login()
    password = ''.join(['Aa0$']+[choice(ascii_letters) for _ in range(6)])
    return email_obj, email, password
    
def CreateAccount(email, password, old_driver=None):
    driver = None
    if type(old_driver) == Chrome:
        driver = old_driver
    else:
        driver_options = ChromeOptions()
        driver_options.add_argument('--headless')
        if os.name == 'posix': # For Linux
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = Chrome(options=driver_options)
        driver.set_window_size(1, 1)

    print('\n[*] [EMAIL] Register page loading...')
    driver.get(f'https://login.eset.com/Register')
    print('[+] [EMAIL] Register page is loaded!')
    driver.execute_script(f"{GET_EBID}('Email').value='{email}'\ndocument.forms[0].submit()")

    print('\n[*] [PASSWD] Register page loading...')
    untilConditionExecute(driver, f"return typeof {GET_EBID}('Password') === 'object'")
    print('[+] [PASSWD] Register page is loaded!')
    driver.execute_script(f"{GET_EBID}('Password').value='{password}'")
    driver.execute_script(f"{GET_EBCN}('input-main input-main--notempty')[0].value='230'\ndocument.forms[0].submit()") # Change Account Region to Ukraine

    is_registed = untilConditionExecute(driver, 'return document.title !== "Service not available" && document.URL === "https://home.eset.com/"')
    if is_registed:
        return driver
    else:
        print('[-] ESET temporarily blocked your IP, try again later!!!')
        driver.quit()

def GetToken(email_obj):
    return eset_intercepter.eset_intercepter(email_obj, DEFAULT_DELAY)

def ConfirmAccount(driver, token):
    print(f'\n[+] ESET Token: {token}')
    print('\n[*] Account confirmation is in progress...')
    driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
    untilConditionExecute(driver, 'return document.title === "ESET HOME"')
    untilConditionExecute(driver, f'return typeof {GET_EBCN}("verification-email_p")[1] === "object"', positive_result=False)
    print('[+] Account successfully confirmed!')
    return True

def CreateALL(print_account_data=False, old_driver=None):
    try:
        driver = None
        if type(old_driver) == Chrome:
            driver = old_driver
        email_obj, email, password = CreateEmailAndPassword()
        driver = CreateAccount(email, password, old_driver=driver)
        if driver is None:
            return None
        token = GetToken(email_obj)
        if print_account_data:
            print(f'\nEmail: {email}\nPassword: {password}')
        ConfirmAccount(driver, token)
        return email, password, driver
    except eset_intercepter.EmailConnectError:
        print('[-] Error connect to server!!!')
    except Exception as E:
        print(f'[-] {E}')
    return None

if __name__ == '__main__':
    if chromeDriverInstallerMenu():
        print('\n-- ESET License Generator {0} --'.format(VERSION))
        data = CreateALL(True)
        if data is None:
            pass
        else:
            data[2].quit()
    input('Press Enter to exit...')