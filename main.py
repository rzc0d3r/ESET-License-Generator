# Version 1.0.4 (12.01.2023)
import eset_license_generator_auto as eset_auto
import time

# ----------- START SETUP -----------

SIZE = 1
OUTPUT = 'eset_accounts.txt'
SLEEP = 1 # in seconds

# ------------ END SETUP ------------

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
            print('[-] Error write account to file!!!')
            break
        print(f'[+] {email}:{password} - written successfully to output file!!!')
    else:
        print('[-] Error get account!!!')
        break
    print(SEP)
    print(f'\n[*] Waiting {SLEEP} seconds\n')
    eset_auto.ClearCookies(driver)
    time.sleep(SLEEP)

driver.quit()   
input('Press Enter...')
