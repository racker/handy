# -*- coding: utf-8 -*-
import csv
from commonfunctions import *

def get_data():
    """Gets Test Data from a csv file"""
    DATA = []
    with open('messages/test_data.csv','rb') as datafile:
        testdata = csv.DictReader(datafile, delimiter = '|')
        for row in testdata:
            DATA.append(row)
    # Replace the for loop below to implement project specific logic
    for row in DATA:
        row['header']  = getheaders(row['header'])
        row['body']  = json.dumps(getbody(row['body']))
        row['url'] = row['url'].replace("<BASE_URL>",BASE_URL)
        row['url'] = row['url'].replace("<longqueuename>",
                                        binascii.b2a_hex(os.urandom(513)))
    return DATA

API_TEST_DATA = get_data()
