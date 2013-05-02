import binascii
import json
import os
import uuid

import config
import http

UUID = str(uuid.uuid1())


def get_keystone_token():
    """Gets Keystone Auth token"""
    req_json = {
                "auth": {
                         "passwordCredentials": {
                                                 "username": config.USERNAME,
                                                 "password": config.PASSWORD
                                                 }
                         },
                }

    header = '{"Host":  "identity.api.rackspacecloud.com",'
    header += '"Content-Type": "application/json","Accept": "application/json"}'
    url = config.AUTH_URL

    response = http.post(url = url, header = header, body = req_json)
    response_body = json.loads(response.text)

    auth_token = response_body["access"]["token"]["id"]
    return auth_token


def create_marconi_headers():
    """Returns headers to be used for all Marconi requests"""
    if config.AUTH_FLAG == "true":
        auth_token = get_keystone_token()
    else:
        auth_token = "notrealtoken"

    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept":  "application/json","Accept-Encoding":  "gzip",'
    headers += '"X-Auth-Token":  "<auth_token>","Client-ID":  "<UUID>"}'
    headers = headers.replace("<auth_token>", auth_token)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USER_AGENT)
    headers = headers.replace("<UUID>", UUID)

    return headers


def invalid_auth_token_header():
    """Returns a header with invalid auth token"""
    auth_token = "0101BLAHBLAHINVALID"

    headers = '{"Host":  "<HOST>","User-Agent":  "<USER-AGENT>","Date":  "<DATE>",'
    headers += '"Accept":  "application/json","Accept-Encoding":  "gzip",'
    headers += '"X-Auth-Token":  "<auth_token>"}'
    headers = headers.replace("<auth_token>", auth_token)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USER_AGENT)

    return headers


def missing_header_fields():
    """Returns a header with missing USER_AGENT header"""
    auth_token = get_keystone_token()

    headers = '{"Host":  "<HOST>","Date":  "<DATE>",'
    headers += '"Accept":  "application/json","Accept-Encoding":  "gzip",'
    headers += '"X-Auth-Token":  "<auth_token>"}'
    headers = headers.replace("<auth_token>", auth_token)
    headers = headers.replace("<HOST>", config.HOST)

    return headers


def plain_text_in_header():
    """Returns headers to be used for all Marconi requests"""
    auth_token = get_keystone_token()

    headers = '{"Host":  "<HOST>","User-Agent":  "<USER-AGENT>","Date":  "<DATE>",'
    headers += '"Accept":  "text/plain","Accept-Encoding":  "gzip",'
    headers += '"X-Auth-Token":  "<auth_token>"}'
    headers = headers.replace("<auth_token>", auth_token)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USER_AGENT)

    return headers


def asterisk_in_header():
    """Returns headers to be used for all Marconi requests"""
    auth_token = get_keystone_token()

    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept":  "*/*","Accept-Encoding":  "gzip",'
    headers += '"X-Auth-Token":  "<auth_token>"}'
    headers = headers.replace("<auth_token>", auth_token)
    headers = headers.replace("<HOST>", config.HOST)
    headers = headers.replace("<USER-AGENT>", config.USER_AGENT)

    return headers


def get_headers(input_header):
    """
    1. If header value is specified in the test_data.csv, that will be used.
    2. Headers can also be substituted in the Robot test case definition
    file (*_tests.txt)
    3. If 1. & 2. is not true -->
      Replaces the header data with generic Marconi headers.
    """
    if input_header:
        header = input_header
    else:
        header = create_marconi_headers()
    return header


def get_custom_body(kwargs):
    """Returns a custom request body"""

    req_body = {"data":  "<DATA>"}
    if "metadatasize" in kwargs.keys():
        random_data = binascii.b2a_hex(os.urandom(kwargs["metadatasize"]))
        req_body["data"] = random_data
    return json.dumps(req_body)


def create_url_from_appender(appender):
    """
    Returns url by catenating the base server with the appender
   appender should have a preceding '/'
   """
    next_url = str(config.BASE_SERVER + appender)
    return(next_url)


def get_url_from_location(header):
    """
    Extracts location from the header.
    returns : the complete url referring to the location
    """
    location = header["location"]
    url = create_url_from_appender(location)
    return url


def verify_metadata(get_data, posted_body):
    """@todo - Really verify the metadata"""
    test_result_flag = False

    get_data = str(get_data)
    posted_body = str(posted_body)
    print(get_data, type(get_data))
    print(posted_body, type(posted_body))
    if get_data in posted_body:
        print("AYYY")
    else:
        test_result_flag = False
        print("NAYYY")

    return test_result_flag
