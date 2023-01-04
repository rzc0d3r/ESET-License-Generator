# Version 1.0.2 (04.01.2023)
import eset_license_generator_auto as eset_auto
import time

# ----------- START SETUP -----------

SIZE = 1
OUTPUT = 'eset_accounts.txt'
SLEEP = 1 # in seconds

# ------------ END SETUP ------------

SEP = '-'*90 # DO NOT TOUCH

for i in range(SIZE):
    print(SEP)
    data = eset_auto.CreateALL()
    if data is not None:
        email, password = data
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
    time.sleep(SLEEP)
    
input('Press Enter...')
