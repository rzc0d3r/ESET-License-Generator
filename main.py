# Version 1.0.1 (31.12.2022)
import eset_license_generator_auto as eset_auto
import time

SIZE = 1
OUTPUT = 'eset_accounts.txt'
SLEEP = 1

for i in range(SIZE):
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
    time.sleep(SLEEP)
    
input('Press Enter...')
