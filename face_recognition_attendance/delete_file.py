import os
import time


# TO DELETE FILE FOR TESTING

def deleteFile():
    if os.path.exists('Excel/client_record.xls'):
        os.remove('Excel/client_record.xls')
    else:
        print('\nPath currently non existent.\n')
        print('Creating path...')


time.sleep(1)
