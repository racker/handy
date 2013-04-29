import binascii
import json
import os
import uuid

import config
import http

UUID = str(uuid.uuid1())


def get_keystone_token():
    """Gets Keystone Auth token"""

    req_json = {"auth":{"passwordCredentials":{"username":config.USERNAME,
                                               "password":config.PASSWORD}}}
    header = '{"Host": "identity.api.rackspacecloud.com",'
    header += '"Content-Type": "application/json","Accept": "application/json"}'
    url = config.AUTH_URL
    response = http.post(url = url, header = header, body = req_json)
    responsebody = json.loads(response.text)
    authtoken = responsebody["access"]["token"]["id"]
    return authtoken


def create_marconi_headers():
    """Returns headers to be used for all Marconi requests"""

    if config.AUTH_FLAG == "true":
        authtoken = get_keystone_token()
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


def invalid_authtoken_header():
    """Returns a header with invalid auth token"""
    authtoken = "0101BLAHBLAHINVALID"
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USERAGENT)
    return headers


def missing_header_fields():
    """Returns a header with missing USERAGENT header"""
    authtoken = get_keystone_token()
    headers = '{"Host": "<HOST>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    return headers


def plain_text_in_header():
    """Returns headers to be used for all Marconi requests"""

    authtoken = get_keystone_token()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "text/plain","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USERAGENT)
    return headers


def asterisk_in_header():
    """Returns headers to be used for all Marconi requests"""

    authtoken = get_keystone_token()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "*/*","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USERAGENT)
    return headers


def get_headers(inputheader):
    """Replacing header data to use Marconi /TestCase specific headers"""
    '''if inputheader:
        customheader = getcustomdata(inputheader)
        if customheader:
            header = customheader
    else:'''
    if inputheader:
        header = inputheader
    else:
        header = create_marconi_headers()
    return header


def get_custom_body(kwargs):
    """Returns a custom requestbody"""
    reqbody = {"data": "<DATA>"}
    if "metadatasize" in kwargs.keys():
        randomdata = binascii.b2a_hex(os.urandom(kwargs["metadatasize"]))
        reqbody["data"] = randomdata
    return json.dumps(reqbody)


def get_body(inputbody):
    """Replacing request data to use Marconi specific body"""
    body = {}
    if inputbody:
        custombody = getcustomdata(inputbody)
        if custombody:
            body = custombody
    else:
        body = inputbody
    return body


def create_url_from_appender(appender):
    """Returns url by catenating the base server with the appender
       - appender should have a preceding / """
    nexturl = str(config.BASE_SERVER + appender)
    return(nexturl)


def get_url_from_location(header):
    location = header["location"]
    url = create_url_from_appender(location)
    return url

