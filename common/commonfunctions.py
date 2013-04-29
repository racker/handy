import http
import json
import os
import binascii
import uuid
#from env import *
import config

UUID = str(uuid.uuid1())


def getkeystonetoken():
    """Gets Keystone Auth token"""

    req_json = {"auth":{"passwordCredentials":{"username":config.USERNAME,"password":config.PASSWORD}}}
    header = '{"Host": "identity.api.rackspacecloud.com","Content-Type": "application/json","Accept": "application/json"}'
    url = config.AUTH_URL
    response = http.post(url = url, header = header, body = req_json)
    responsebody = json.loads(response.text)
    authtoken = responsebody["access"]["token"]["id"]
    return authtoken


def createmarconiheaders():
    """Returns headers to be used for all Marconi requests"""

    if config.AUTH_FLAG == "true":
        authtoken = getkeystonetoken()
    else:
        authtoken = "notrealtoken"
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>","Client-ID": "<UUID>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USERAGENT)
    headers = headers.replace("<UUID>", UUID)

    return headers


def invalidauthtokenheader():
    """Returns a header with invalid auth token"""
    authtoken = "0101BLAHBLAHINVALID"
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USERAGENT)
    return headers


def missingheaderfields():
    """Returns a header with missing USERAGENT header"""
    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    return headers


def plaintextinheader():
    """Returns headers to be used for all Marconi requests"""

    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "text/plain","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USERAGENT)
    return headers


def asteriskinheader():
    """Returns headers to be used for all Marconi requests"""

    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "*/*","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USERAGENT)
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


def getcustombody(kwargs):
    """Returns a custom requestbody"""
    reqbody = {"data": "<DATA>"}
    if "metadatasize" in kwargs.keys():
        randomdata = binascii.b2a_hex(os.urandom(kwargs["metadatasize"]))
        reqbody["data"] = randomdata
    return json.dumps(reqbody)


def getbody(inputbody):
    """Replacing request data to use Marconi specific body"""
    body = {}
    if inputbody:
        custombody = getcustomdata(inputbody)
        if custombody:
            body = custombody
    else:
        body = inputbody
    return body


def createurlfromappender(appender):
    """Returns url by catenating the base server with the appender
       - appender should have a preceding / """
    nexturl = str(config.BASE_SERVER + appender)
    return(nexturl)


def geturlfromlocation(header):
    location = header["location"]
    url = createurlfromappender(location)
    return url

