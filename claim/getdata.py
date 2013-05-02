# -*- coding: utf-8 -*-
import csv

import common

def get_data():
    """Reads the test data from claim/test_data.csv"""
    DATA = []
    with open('claim/test_data.csv','rb') as datafile:
        testdata = csv.DictReader(datafile, delimiter = '|')
        for row in testdata:
            DATA.append(row)
    for row in DATA:
        row['header']  = common.functionlib.get_headers(row['header'])
        row['url'] = row['url'].replace("<BASE_URL>",common.config.BASE_URL)
    return DATA

API_TEST_DATA = get_data()
