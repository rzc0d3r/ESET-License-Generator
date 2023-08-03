# Version: 1.0.3 (03.08.2023)
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

import os
import time

def until_code_execute(driver, js, timeout, max_iter, positive_result='OK'):
    i = 0
    while True:
        try:
            if i > max_iter:
                return False
            result = driver.execute_script('\n'.join(js))
            if result == positive_result:
                return True
        except:
            pass
        i += 1
        time.sleep(timeout)

def eset_login(email, password):
    driver_options = ChromeOptions()
    if os.name == 'posix': # For Linux
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')
    driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = Chrome(service=Service('chromedriver.exe'), options=driver_options)
    driver.set_window_size(600, 800)

    driver.get('https://login.eset.com/Login')
    if until_code_execute(driver, ["if (document.getElementsByClassName('account__entry btn btn-normal').length > 0) {return 'OK'}"], 1, 10):
        js = [
            f"document.getElementById('Email').value = '{email}'",
            f"document.getElementById('Password').value = '{password}'",
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
            password_error_text = driver.execute_script("return document.getElementById('Password-error').innerText")
            if password_error_text != '': # Other information from 'Password-error' object about incorrect login data
                status_login = False
        except:
            status_login = True
    return driver, status_login

if __name__ == '__main__':
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
