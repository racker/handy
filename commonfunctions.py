import httpfnlib
import json
import os
import binascii
import random
import sys
import uuid
from env import  *

UUID = str(uuid.uuid1())

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
    headers += '"X-Auth-Token": "<AuthToken>","Client-ID": "<UUID>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", HOST)
    headers = headers.replace("<USER-AGENT>", USERAGENT)
    headers = headers.replace("<UUID>", UUID)

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

def getheaders(inputheader):
    """Replacing header data to use Marconi /TestCase specific headers"""
    if inputheader:
        customheader = getcustomdata(inputheader)
        if customheader:
            header = customheader
    else:
        header = createmarconiheaders()
    return header

def getcustomdata(handydict):
    """Returns custom data as specified in test data"""
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
        elif ("messagecount" in functiontocall.keys()):
            customdata = getmessagebody(**functiontocall)
        elif ("metadatasize" in functiontocall.keys()):
            customdata = getcustombody(**functiontocall)
        return customdata
    else:
        return handydict


def getcustombody(**kwargs):
    """Returns a custom requestbody"""
    data = kwargs
    if "metadatasize" in kwargs.keys():
        data = binascii.b2a_hex(os.urandom(kwargs["metadatasize"]))
    return data

def getbody(inputbody):
    """Replacing request data to use Marconi specific headers"""
    body = {}
    if inputbody:
        custombody = getcustomdata(inputbody)
        if custombody:
            body = custombody
    else:
        body = inputbody
    return body

