# -*- coding: utf-8 -*-
import csv
import common

def get_data():
    """Gets Test Data from a csv file"""
    DATA = []
    with open('queue/test_data.csv','rb') as datafile:
        testdata = csv.DictReader(datafile, delimiter = '|')
        for row in testdata:
            DATA.append(row)
    for row in DATA:
        row['url'] = row['url'].replace("<BASE_URL>", common.config.BASE_URL)
    return DATA

API_TEST_DATA = get_data()
