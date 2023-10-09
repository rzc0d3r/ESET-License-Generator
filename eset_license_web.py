# Version: 1.0.3.2 (101023-0017)
VERSION = 'v1.0.3.2 (101023-0017) by rzc0d3r'
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from modules.shared_tools import *

import os

def eset_login(email, password):
    driver_options = ChromeOptions()
    if os.name == 'posix': # For Linux
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')
    driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = Chrome(options=driver_options)
    driver.set_window_size(600, 800)

    driver.get('https://login.eset.com/Login')
    if untilConditionExecute(driver, f"return {GET_EBCN}('input-main text-box single-line').length > 0"):
        js = [
            f"{GET_EBCN}('input-main text-box single-line')[0].value = '{email}'",
            f"{GET_EBCN}('password-input text-box single-line password')[0].value = '{password}'",
            f"document.forms[0].submit()"
        ]
        driver.execute_script('\n'.join(js))
    else:
        print('[-] Analysis error!!!')
        status_login = False
    title = driver.execute_script('return document.title') # critical incorrect login data (Site crash)
    if title == 'Service not available':
        status_login = False
    else: # if 'Password-error' object is exists -> incorrect login data, if 'Password-error' object is missing - no problem (correct login data)
        try:
            password_error_text = driver.execute_script(f"return {GET_EBID}('Password-error').innerText")
            if password_error_text != '': # Other information from 'Password-error' object about incorrect login data
                status_login = False
        except:
            status_login = True
    return driver, status_login

if __name__ == '__main__':
    if chromeDriverInstallerMenu():
        print('\n-- ESET License Generator {0} --\n'.format(VERSION))
        email = input('ESET Account Email: ').strip()
        password = input('ESET Account Password: ').strip()
        driver, status_login = eset_login(email, password)
        if status_login:
            print('\n[+] Successuful login!!!')
            driver.get('https://home.eset.com/licenses')
            input('\nPress Enter if you have deleted licenses...')
        else:
            print('\n[-] Incorrect login data!!!')
            input('\nPress Enter...')
        driver.quit()