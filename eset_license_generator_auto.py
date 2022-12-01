import eset_intercepter as ESET
import selenium.webdriver
import random
import string

def CreateEmailAndPassword():
    email_obj = ESET.Email()
    email_obj.register()
    email = email_obj.get_full_login()
    password = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice('0123456789')]
    password += [random.choice(string.ascii_letters+'0123456789') for _ in range(17)]
    password = ''.join(password)
    return email_obj, email, password
    
def CreateAccount(email, password):
    driver = selenium.webdriver.Edge('msedgedriver.exe')
    driver.minimize_window()
    driver.get(f'https://login.eset.com/Register?e={email}&p={password}')
    js = [
        f"document.getElementById('Email').value = '{email}'",
        f"document.getElementById('Password').value = '{password}'",
        "document.forms[0].submit()"
    ]
    driver.execute_script('\n'.join(js))
    return driver

def GetToken(email_obj):
    return ESET.ESETIntercepter(email_obj)

def ConfirmAccount(driver, token):
    driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
    driver.quit()

def CreateALL():
    email_obj, email, password = CreateEmailAndPassword()
    driver = CreateAccount(email, password)
    token = GetToken(email_obj)
    print(f'\n[+] ESET Token: {token}')
    ConfirmAccount(driver, token)
    print(f'\nEmail: {email}\nPassword: {password}')
    return email, password

if __name__ == '__main__':
    CreateALL()
    input('Press Enter...')
