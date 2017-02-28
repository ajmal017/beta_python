'''
This is main file for driving the IB onboarding process.

If necessary, it can be run with test data from the Django context with the
command './manage.py onboard_test_00'.

There are also various utlities available,which can be run with a similar
command (e.g. './manage.py onboard_utility_clean_directories'):
- onboard_utility_clean_directories.py
- onboard_utility_delete_a_key.py
- onboard_utility_delete_keys.py
- onboard_utility_gen_public_key.py
- onboard_utility_ib_ftp_delete_a_file.py
- onboard_utility_ib_ftp_delete_files.py
- onboard_utility_ib_ftp_list_files.py
- onboard_utility_import_a_key.py
- onboard_utility_list_keys.py
- onboard_utility_xml_show.py

'''

import os
import pandas as pd
from pytz import common_timezones
from ftplib import FTP
import shutil
import xml.etree.ElementTree as ET
import pdb

from onboarding.interactive_brokers import compression as zp
from onboarding.interactive_brokers import encryption as encr
from onboarding.interactive_brokers import ib_onboard_customer as ib_cust
from onboarding.interactive_brokers import onboard_individual as individual
from onboarding.interactive_brokers import onboarding_helpers as onb_help

DEBUG = True

# for IB filename
TIMEZONE_BETASMARTZ = 'Australia/Sydney'
TIMEZONE_IB = 'America/New_York'

# paths
PATH_TO_FILES = os.getcwd() + '/onboarding/interactive_brokers/Files/'
UNCOMPRESSED = 'uncompressed/'
ZIPPED = 'zipped/'
ENCRYPTED = 'encrypted/'
KEYS = 'Keys/'
DOCUMENTS = 'documents/'

DIRS = (PATH_TO_FILES + UNCOMPRESSED,
        PATH_TO_FILES + ZIPPED,
        PATH_TO_FILES + ENCRYPTED,)

# agreements and disclosures
DOCS = ( 'Form1005.pdf',  'Form2192.pdf',  'Form3071.pdf',
         'Form4036.pdf',  'Form9130.pdf',  'Form2109.pdf',
         'Form3070.pdf',  'Form4016.pdf',  'Form4070.pdf',)

TAXFORMS = ('Form5001.pdf', 'Form5002.pdf',
            'Form5006.pdf', 'Form5017.pdf',)

# xml
URI = '{http://www.interactivebrokers.com/schemas/IBCust_import}'
ENCODING = 'US-ASCII'
STANDALONE='yes'

# encryption
IB_PUBLIC_KEY = 'IBKR_CI.PubKey.asc'
IB_UIDS = 'CI Interactive Brokers <ci@interactivebrokers.com>'
BETASMARTZ_PUBLIC_KEY = 'BetaSmartz.PubKey.asc'
BETASMARTZ_UIDS = 'BetaSmartz (ECA Key) <ib_onboarding@betasmartz.com>'

# ftp
IB_FTP = 'ftp.interactivebrokers.com'
FTP_DIR = 'applications/incoming'
FTP_USERNAME = 'btta95ibs2'
FTP_PASSWORD = 'smar37zxe8'


def onboard(onboarding):
    '''
    returns Truec if successfully completes create object for a single customer,
    create xml tree, write to file, zip, encrypt, then ftp to IB ftp site
    '''
    try:
        for d in DIRS:
            if os.path.exists(d):
                shutil.rmtree(d)
            os.makedirs(d)

        tree = individual.get_tree(onboarding,
                                   DOCS,
                                   TAXFORMS)

        if DEBUG:
            onb_help.show_tree(tree.getroot())
            print('---------------- set DEBUG=False to hide this ^^^^^^')
        
        ib_onboard_file_name = get_ib_onboard_file_name()

        tree.write(PATH_TO_FILES + UNCOMPRESSED + ib_onboard_file_name + '.xml',
                   encoding=ENCODING,
                   xml_declaration=True)
        

        for doc in DOCS + TAXFORMS:
            shutil.copy(PATH_TO_FILES + DOCUMENTS + doc, PATH_TO_FILES + UNCOMPRESSED)

        zip_file = ib_onboard_file_name + '.zip'
        zp.zip_file(PATH_TO_FILES, UNCOMPRESSED, ZIPPED, zip_file)

        encr.encrypt(PATH_TO_FILES,
                     ZIPPED, KEYS,
                     ENCRYPTED,
                     BETASMARTZ_UIDS,
                     IB_UIDS,
                     zip_file)

        ftp = FTP(IB_FTP)
        ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)
        ftp.cwd(FTP_DIR)

        if DEBUG:
            get_ib_ftp_file_list('before', ftp)
            print('---------------- set DEBUG=False to hide this ^^^^^^')

        path = PATH_TO_FILES + ENCRYPTED
        file_to_send =  zip_file + '.gpg'
        upload(ftp, path, file_to_send)

        if DEBUG:
            get_ib_ftp_file_list('after', ftp)
            print('---------------- set DEBUG=False to hide this ^^^^^^')

        return True
    except:
        return False


def get_current_ib_time():
    '''
    returns current time measured in BetaSmartz production servers but
    converted to IB timezone
    '''
    current_betasmartz_ts = pd.Timestamp('today', tz=TIMEZONE_BETASMARTZ)
    return current_betasmartz_ts.tz_convert(TIMEZONE_IB)


def get_ib_ftp_file_list(text, ftp):
    '''
    prints list of files in current IB ftp working directory
    '''
    data = []
    ftp.dir(data.append)
    files=[]
    file_tail = '.zip.gpg'
    for i in range(len(data)):
        files = files + [elem for elem in data[i].split(' ') if len(elem) > len(file_tail) and elem[-len(file_tail):] == file_tail]
    print('files ', text, ' ftp upload:', files)


def get_ib_onboard_file_name():
    '''
    returns file name in format specified by Interactive Brokers for onboarding
    '''

    hr_start = '03'
    mint_start = '01'
    sec_start = '00'
    
    current_ib_ts = get_current_ib_time()
    ib_ts_for_earliest_val_bus_day = get_ts_for_earliest_valid_business_day(current_ib_ts)

    if ib_ts_for_earliest_val_bus_day.time().hour <= 3:
        yr = str(ib_ts_for_earliest_val_bus_day.date().year)
        mnth = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().month)
        dy = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().day)
        hr = hr_start
        mint = mint_start
        sec = sec_start

    elif ib_ts_for_earliest_val_bus_day.time().hour == 16 and ib_ts_for_earliest_val_bus_day.time().minute > 9:
        ib_ts_for_earliest_val_bus_day = ib_ts_for_earliest_val_bus_day.date() + pd.DateOffset(days=1)
        yr = str(ib_ts_for_earliest_val_bus_day.date().year)
        mnth = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().month)
        dy = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().day)
        hr = hr_start
        mint = mint_start
        sec = sec_start

    elif ib_ts_for_earliest_val_bus_day.time().hour >= 16:
        ib_ts_for_earliest_val_bus_day = ib_ts_for_earliest_val_bus_day.date() + pd.DateOffset(days=1)
        yr = str(ib_ts_for_earliest_val_bus_day.date().year)
        mnth = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().month)
        dy = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().day)
        hr = hr_start
        mint = mint_start
        sec = sec_start

    else:
        yr = str(ib_ts_for_earliest_val_bus_day.date().year)
        mnth = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().month)
        dy = set_as_2_chars(ib_ts_for_earliest_val_bus_day.date().day)
        hr = set_as_2_chars(ib_ts_for_earliest_val_bus_day.time().hour)
        mint = set_as_2_chars(ib_ts_for_earliest_val_bus_day.time().minute)
        sec = set_as_2_chars(ib_ts_for_earliest_val_bus_day.time().second)

    file_name = 'BetaSmartz_' + yr + '-' + mnth + '-' + dy + '_' + hr + mint + sec

    return file_name


def get_modified_root(root, cust_obj):
    '''
    modifies root with values held on cust_obj attributes
    '''
    root = individual.get_modified_root_individual(root, cust_obj)
    return root


def get_ts_for_earliest_valid_business_day(ts_ib):
    '''
    returns timestamp adjusted if necessary for earliest weekday between hours
    specified by IB for onboarding.

    2017-03_06: "Notes: In production, the automation step's run time is from 3:00am to
    16:10pm EST. So if you posted a file at 8PM EST tonight, for example, please
    make sure the naming convention date is 2017-03-07. If you post a file over
    the weekend, you will want to use Monday’s date with a time stamp after 3AM EST."
    '''
    if ts_ib.dayofweek == 6:
        ts_ib = ts_ib.date() + pd.DateOffset(days=1)

    elif ts_ib.dayofweek == 5:
        ts_ib = ts_ib.date() + pd.DateOffset(days=2)

    elif ts_ib.dayofweek == 4 and ts_ib.time().hour >= 16 and ts_ib.time().minute >= 0:
        ts_ib = ts_ib.date() + pd.DateOffset(days=1)

    return ts_ib


def set_as_2_chars(c):
    '''
    single digit times (i.e. h, m or s) or dates (i.e. d) are given a preceding '0'
    so that they are exactly two characters long.
    '''
    try:
        if c < 10:
            cc = '0' + str(c)
        else:
            cc = str(c)
        return cc
    except:
        raise Exception('c not handled:' + str(c))


def upload(ftp, path, file):
    '''
    ftp uploads given file located at given path
    '''
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file, open(path + file))
    else:
        ftp.storbinary("STOR " + file, open(path + file, "rb"))
