# -*- coding: utf-8 -*-
import csv
import httpfnlib
import json
import os
import binascii


#START ENVIRONMENT VARIABLES
HOST = "marconi.test.com"
USERAGENT = "useragent"
AUTH_URL = "https://identity.api.rackspacecloud.com/v2.0/tokens"
MARCONI_SERVER = "166.78.150.92:8888"
#END ENVIRONMENT VARIABLES

#START CUSTOM FUNCTIONS
def getkeystonetoken():
    """Gets Keystone Auth token"""

    req_json = '{"auth":{"passwordCredentials":{"username":"","password":""}}}'
    header = '{"Host": "identity.api.rackspacecloud.com","Content-Type": "application/json","Accept": "application/json"}'
    url = AUTH_URL
    response = httpfnlib.httppost(url = url,header = header, body = req_json)
    responsebody = json.loads(response.text)
    authtoken = responsebody["access"]["token"]["id"]
    return authtoken

def createmarconiheaders():
    """Returns headers to be used for all Marconi requests"""

    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", HOST)
    headers = headers.replace("<USER-AGENT>", USERAGENT)
    return headers

def invalidauthtokenheader():
    """Returns a header with invalid auth token"""
    authtoken = "0101BLAHBLAHINVALID"
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", HOST)
    headers = headers.replace("<USER-AGENT>", USERAGENT)
    return headers

def missingheaderfields():
    """Returns a header with invalid auth token"""
    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", HOST)
    headers = headers.replace("<USER-AGENT>", USERAGENT)
    return headers

def plaintextinheader():
    """Returns headers to be used for all Marconi requests"""

    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "text/plain","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", HOST)
    headers = headers.replace("<USER-AGENT>", USERAGENT)
    return headers

def asteriskinheader():
    """Returns headers to be used for all Marconi requests"""

    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "*/*","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", HOST)
    headers = headers.replace("<USER-AGENT>", USERAGENT)
    return headers

def getcustombody(**kwargs):
    """Returns a custom requestbody"""
    data = kwargs
    if "metadatasize" in kwargs.keys():
        data = binascii.b2a_hex(os.urandom(kwargs["metadatasize"]))
    return data

def getcustomdata(handydict):
    handydict = json.loads(handydict)
    customflag = "HANDYFLAG" in handydict.keys()
    if customflag:
        functiontocall = handydict["HANDYFLAG"]
        if functiontocall == "invalidauthtokenheader":
            customdata = invalidauthtokenheader()
        elif functiontocall == "missingheaderfields":
            customdata = missingheaderfields()
        elif functiontocall == "plaintextinheader":
            customdata = plaintextinheader()
        elif functiontocall == "asteriskinheader":
            customdata = asteriskinheader()
        elif functiontocall == "metadatasize4097":
            customdata = getcustombody(metadatasize = 4097)
        elif functiontocall == "metadatasize4096":
            customdata = getcustombody(metadatasize = 4096)
        elif functiontocall == "metadatasize4095":
            customdata = getcustombody(metadatasize = 4095)
        return customdata
    else:
        return handydict

def getheaders(inputheader):
    """Replacing header data to use Marconi /TestCase specific headers"""
    if inputheader:
        customheader = getcustomdata(inputheader)
        if customheader:
            header = customheader
    else:
        header = createmarconiheaders()
    return header

def getbody(inputbody):
    """Replacing header data to use Marconi specific headers"""
    body = {}
    if inputbody:
        custombody = getcustomdata(inputbody)
        if custombody:
            body = custombody
    else:
        body = inputbody
    return body

#END CUSTOM FUNCTIONS

#GET TEST DATA
def get_data():
    """Gets Test Data from a csv file"""
    DATA = []
    with open('queue/test_data.csv','rb') as datafile:
        testdata = csv.DictReader(datafile, delimiter = '|')
        for row in testdata:
            DATA.append(row)
    # Replace the for loop below to implement project specific logic
    for row in DATA:
        row['header']  = getheaders(row['header'])
        row['body']  = json.dumps(getbody(row['body']))
        row['url'] = row['url'].replace("<SERVER>",MARCONI_SERVER)
        row['url'] = row['url'].replace("<longqueuename>",
                                        binascii.b2a_hex(os.urandom(513)))
    return DATA

API_TEST_DATA = get_data()
#getcustombody(metadatasize = 1)
#END TEST DATA
