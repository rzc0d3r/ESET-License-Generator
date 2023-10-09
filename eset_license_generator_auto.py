# Version: 1.0.8.2 (09.10.2023)
import eset_intercepter
import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from string import ascii_letters
from random import choice

from eset_license_web import until_code_execute

import os

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
        if os.name == 'posix': # For Linux
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
            driver_options.add_argument('--headless')
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = Chrome(options=driver_options)
        driver.set_window_size(1, 1)

    driver.get(f'https://login.eset.com/Register')
    getbyid = 'document.getElementById'
    driver.execute_script(f"{getbyid}('Email').value='{email}'\ndocument.forms[0].submit()")

    while True:
        time.sleep(0.1)
        title = driver.execute_script(f"return {getbyid}('Password')")
        if title != None:
            break

    driver.execute_script(f"{getbyid}('Password').value='{password}'")
    driver.execute_script(f"{getbyid}('input-main input-main--notempty')[0].value='230'\ndocument.forms[0].submit()") # Change Account Region to Ukraine

    while True:
        time.sleep(0.1)
        title = driver.execute_script('return document.title')
        if title == 'Service not available':
            print('[-] ESET temporarily blocked your IP, try again later!!!')
            driver.quit()
            break
        url = driver.execute_script('return document.URL')
        if url == 'https://home.eset.com/':
            return driver
    return None

def ClearCookies(driver):
    driver.delete_all_cookies()

def GetToken(email_obj):
    return eset_intercepter.eset_intercepter(email_obj, 0.5)

def ConfirmAccount(driver, token):
    driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
    until_code_execute(driver, ['return document.title === "ESET HOME"'], 1, 30, positive_result=True)
    until_code_execute(driver, [f'return typeof document.getElementsByClassName("verification-email_p")[1] === "object"'], 1, 30, positive_result=False)
    
def CreateALL(print_eset_token=True, print_account_data=False, old_driver=None):
    try:
        driver = None
        if type(old_driver) == Chrome:
            driver = old_driver
        email_obj, email, password = CreateEmailAndPassword()
        driver = CreateAccount(email, password, old_driver=driver)
        if driver is None:
            return None
        token = GetToken(email_obj)
        if print_eset_token:
            print(f'\n[+] ESET Token: {token}')
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
    data = CreateALL(True, True)
    if data is None:
        pass
    else:
        data[2].quit()
    input('Press Enter...')
