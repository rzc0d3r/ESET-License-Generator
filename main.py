# Version 1.0.5 (101023-0017)
import eset_license_generator_auto as eset_auto
from modules.shared_tools import chromeDriverInstallerMenu
import time

# ----------- START SETUP -----------

SIZE = 1
OUTPUT = 'eset_accounts.txt'
SLEEP = 1 # in seconds

# ------------ END SETUP ------------
if not chromeDriverInstallerMenu():
    exit(-1)
print('\n-- ESET License Generator {0} --\n'.format(eset_auto.VERSION))

SEP = '-'*65 # DO NOT TOUCH

driver = None
for i in range(SIZE):
    print(SEP)
    data = eset_auto.CreateALL(old_driver=driver)
    if data is not None:
        email, password = data[0], data[1]
        driver = data[2]
        try:
            f = open(OUTPUT, 'a')
            f.write(f'{email} : {password}\n')
            f.close()
        except:
            print('\n[-] Error write account to file!!!')
            break
        print(f'\n[+] {email}:{password} - written successfully to output file!!!')
    else:
        print('\n[-] Error get account!!!')
        break
    print(SEP)
    print(f'\n[*] Waiting {SLEEP} seconds\n')
    driver.delete_all_cookies()
    time.sleep(SLEEP)

driver.quit()   
input('Press Enter...')