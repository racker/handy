# -*- coding: utf-8 -*-
import csv

import common

def get_data():
    """Gets Test Data from a csv file"""
    DATA = []
    with open('messages/test_data.csv','rb') as datafile:
        test_data = csv.DictReader(datafile, delimiter = '|')
        for row in test_data:
            DATA.append(row)
    for row in DATA:
        row['header']  = common.functionlib.get_headers(row['header'])
        row['url'] = row['url'].replace("<BASE_URL>",common.config.BASE_URL)
    return DATA


API_TEST_DATA = get_data()