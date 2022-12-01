import eset_license_generator_auto as eset_auto
import time

SIZE = 1
OUTPUT = 'eset_accounts.txt'
SLEEP = 5


for i in range(SIZE):
    email, password = eset_auto.CreateALL()
    f = open(OUTPUT, 'a')
    f.write(f'{email} : {password}\n')
    f.close()
    time.sleep(SLEEP)
input('Press Enter...')