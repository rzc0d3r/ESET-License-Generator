# Version: 1.0.7 (12.01.2023)
import eset_intercepter
import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from string import ascii_letters
from random import choice

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
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = Chrome(service=Service('chromedriver.exe'), options=driver_options)
        driver.set_window_size(1, 1)

    driver.get(f'https://login.eset.com/Register')
    submit, getbyid = 'document.forms[0].submit()', 'document.getElementById'
    driver.execute_script(f"{getbyid}('Email').value='{email}'\n{submit}")

    while True:
        time.sleep(0.1)
        title = driver.execute_script(f"return {getbyid}('Password')")
        if title != None:
            break

    driver.execute_script(f"{getbyid}('Password').value='{password}'\n{submit}")

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
