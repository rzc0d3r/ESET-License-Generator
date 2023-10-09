# Version: 1.0 (101023-0017)
from subprocess import check_output, PIPE
from time import sleep

import os
import modules.chrome_driver_installer as chrome_driver_installer

GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'
DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1

def untilConditionExecute(driver, js: str, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True):
    i = 0
    while True:
        try:
            if i > max_iter:
                return False
            result = driver.execute_script(js)
            if result == positive_result:
                return True
        except Exception as E:
            pass
        i += 1
        sleep(delay)

def chromeDriverInstallerMenu():
    try:
        # auto updating or installing chrome driver
        print('-- Chrome Driver Auto-Installer {0} --\n'.format(chrome_driver_installer.VERSION))
        chrome_version, _, chrome_major_version, _, _ = chrome_driver_installer.get_chrome_version()
        if chrome_version is None:
            print('[-] Chrome is not detected on your device!')
            raise RuntimeError
        current_chromedriver_version = None
        platform, arch = chrome_driver_installer.get_platform_for_chrome_driver()
        chromedriver_name = 'chromedriver.exe'
        if platform != 'win':
            chromedriver_name = 'chromedriver'
        if os.path.exists(chromedriver_name):
            os.chmod(chromedriver_name, 0o777)
            out = check_output([chromedriver_name, "--version"], stderr=PIPE)
            if out is not None:
                current_chromedriver_version = out.decode("utf-8").split(' ')[1]
        print('[*] Chrome version: {0}'.format(chrome_version))
        print('[*] Chrome driver version: {0}'.format(current_chromedriver_version))
        if current_chromedriver_version is None:
            print('\n[-] Chrome driver not detected, download attempt...')
        elif current_chromedriver_version.split('.')[0] != chrome_version.split('.')[0]: # major version match
            print('\n[-] Chrome driver version doesn\'t match version of the installed chrome, trying to update...')
        if current_chromedriver_version is None or current_chromedriver_version.split('.')[0] != chrome_version.split('.')[0]:
            driver_url = chrome_driver_installer.get_driver_download_url()
            if driver_url is None:
                print('\n[-] Couldn\'t find the right version for your system!')
                method = input('\nRun the program anyway? (y/n): ')
                if method == 'n':
                    exit(-1)
                    return False
            else:
                print('\n[+] Found a suitable version for your system!')
                print('\n[*] Download attempt...')
                if chrome_driver_installer.download_chrome_driver('.', driver_url):
                    print('[+] The Сhrome driver was successfully downloaded and unzipped!')
                    input('\nPress Enter to continue...')
                else:
                    print('[-] Error downloading or unpacking!')
                    method = input('\nRun the program anyway? (y/n): ')
                    if method == 'n':
                        exit(-1)
                        return False
    except Exception as E:
        print(E)
        return False
    return True