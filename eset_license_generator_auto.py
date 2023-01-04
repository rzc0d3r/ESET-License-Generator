# Version: 1.0.4 (05.01.2023)
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
    
def CreateAccount(email, password):
    driver_options = ChromeOptions()
    driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = Chrome(service=Service('chromedriver.exe'), options=driver_options)
    driver.minimize_window()

    driver.get(f'https://login.eset.com/Register')
    submit, getbyid = 'document.forms[0].submit()', 'document.getElementById'
    driver.execute_script(f"{getbyid}('Email').value='{email}'\n{submit}")
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

def GetToken(email_obj):
    return eset_intercepter.eset_intercepter(email_obj, 0.5)

def ConfirmAccount(driver, token):
    driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
    driver.quit()

def CreateALL(print_eset_token=True, print_account_data=False):
    try:
        email_obj, email, password = CreateEmailAndPassword()
        driver = CreateAccount(email, password)
        if driver is None:
            return None
        token = GetToken(email_obj)
        if print_eset_token:
            print(f'\n[+] ESET Token: {token}')
        if print_account_data:
            print(f'\nEmail: {email}\nPassword: {password}')
        ConfirmAccount(driver, token)
        return email, password
    except eset_intercepter.EmailConnectError:
        print('[-] Error connect to server!!!')
    except Exception as E:
        print(f'[-] {E}')
    return None

if __name__ == '__main__':
    CreateALL(True, True)
    input('Press Enter...')
