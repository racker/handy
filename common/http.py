# -*- coding: utf-8 -*-
import requests
import json

def get(url, header = '', param = ''):
    """Function to perform http GET"""
    if header:
    #@todo2
        header = json.loads(header)
    try:
        response = requests.get(url, headers = header, params = param)
    except requests.ConnectionError as detail:
        print("ConnectionError: Exception in httpget {}".format(detail))
    except requests.HTTPError as detail:
        print("HTTPError: Exception in httpget {}".format(detail))
    except requests.Timeout as detail:
        print("Timeout: Exception in httpget {}".format(detail))
    except requests.TooManyRedirects as detail :
        print("TooManyRedirects: Exception in httpget {}".format(detail))
    return response


def post(url, header = '', body = '', param = ''):
    """Function to perform http POST"""
    if header:
    #@todo2
        header = json.loads(header)
    body = str(body)
    body = body.replace("'",'"')
    try:
        response = requests.post(url, headers = header, data = body,
                                 params = param)
    except requests.ConnectionError as detail:
        print("ConnectionError: Exception in httppost {}".format(detail))
    except requests.HTTPError as detail:
        print("HTTPError: Exception in httppost {}".format(detail))
    except requests.Timeout as detail:
        print("Timeout: Exception in httppost {}".format(detail))
    except requests.TooManyRedirects as detail :
        print("TooManyRedirects: Exception in httppost {}".format(detail))
    return response


def put(url, header = '', body = '', param = ''):
    """Function to perform http PUT"""
    response = None
    if header:
        header = json.loads(header)
    try:
        response = requests.put(url, headers = header, data = body,
                                 params = param)
    except requests.ConnectionError as detail:
        print("ConnectionError: Exception in httpput {}".format(detail))
    except requests.HTTPError as detail:
        print("HTTPError: Exception in httpput {}".format(detail))
    except requests.Timeout as detail:
        print("Timeout: Exception in httpput {}".format(detail))
    except requests.TooManyRedirects as detail :
        print("TooManyRedirects: Exception in httpput {}".format(detail))
    return response


def delete(url, header = '', param = ''):
    """Function to perform http DELETE"""
    response = None
    if header:
    #@todo2
        header = json.loads(header)
    try:
        response = requests.delete(url, headers = header, params = param)
    except requests.ConnectionError as detail:
        print("ConnectionError: Exception in httpdelete {}".format(detail))
    except requests.HTTPError as detail:
        print("HTTPError: Exception in httpdelete {}".format(detail))
    except requests.Timeout as detail:
        print("Timeout: Exception in httpdelete {}".format(detail))
    except requests.TooManyRedirects as detail :
        print("TooManyRedirects: Exception in httpdelete {}".format(detail))
    return response

def patch(url, header = '', body = '', param = ''):
    """Function to perform http PATCH"""
    response = None
    if header:
        header = json.loads(header)
    try:
        response = requests.patch(url, headers = header, data = body,
                                 params = param)
    except requests.ConnectionError as detail:
        print("ConnectionError: Exception in httppatch {}".format(detail))
    except requests.HTTPError as detail:
        print("HTTPError: Exception in httppatch {}".format(detail))
    except requests.Timeout as detail:
        print("Timeout: Exception in httppatch {}".format(detail))
    except requests.TooManyRedirects as detail :
        print("TooManyRedirects: Exception in httppatch {}".format(detail))
    return response


def executetests(row):
    """Executes the tests defined in the API_TESTS.txt & data.csv"""
    httpverb = row['httpverb'].strip()
    url = row['url']
    header = row['header']
    params = row['params']
    body = row['body']
    expectedRC = row['expectedRC']
    expectedRC = int(expectedRC)
    expectedresponsebody = row['expectedResponseBody']
    response = None

    if httpverb == 'GET' :
        response = get(url, header, params)
    elif httpverb == 'POST' :
        response = post(url, header, body, params)
    elif httpverb == 'PUT' :
        response = put(url, header, body, params)
    elif httpverb == 'DELETE' :
        response = delete(url, header, params)
    elif httpverb == 'PATCH' :
        response = patch(url, header, body, params)
    if response != None:
        testresultflag = verifyresponse(response, expectedRC, expectedresponsebody)
    else:
        testresultflag = False

    if not testresultflag :
        print httpverb
        print(url)
        print(header)
        print(body)
        print("Actual Response: {}".format(response.status_code))
        print("Actual Response Headers")
        print response.headers
        print("Actual Response Body")
        print response.text
        print("ExpectedRC: {}".format(expectedRC))
        print("expectedresponsebody: {}".format(expectedresponsebody))
        assert testresultflag,"Actual Response does not match the Expected"
    else:
        #print response
        return response.headers, response.text



def verifyresponse(response, expectedRC, expectedresponsebody):
    """Compares the http Response with the expected Response"""
    testresultflag = True
    actualRC = response.status_code
    actualresponsebody = response.text
    if actualRC == expectedRC :
        if expectedresponsebody:
            compareresponsebody(expectedresponsebody, actualresponsebody)
    else:
        testresultflag = False
        print("Unexpected http Response code {}".format(actualRC))
        print "Response Body returned"
        print actualresponsebody
    return testresultflag


def compareresponsebody(expectedresponsebody, actualresponsebody):
    """Compare the response body of a http request with the expected """
    testresultflag = True
    #@todo2
    try:
        expectedresponsebody = json.loads(expectedresponsebody)
    except ValueError as detail :
        print("ValueError: In json.loads(expectedresponsebody)".format(detail))
    try:
        actualresponsebody = json.loads(actualresponsebody)
    except ValueError as detail :
        print("ValueError: In json.loads(actualresponsebody)".format(detail))
    diff = ""
    try:
        diff = set(expectedresponsebody) - set(actualresponsebody)
    except TypeError as detail:
        print("TypeError: Exception in compareresponsebody {}".format(detail))
        return
    if diff:
        print(diff)
        testresultflag = False
    else:
        testresultflag = compareresponsebodydata(expectedresponsebody, actualresponsebody)
    return testresultflag


def compareresponsebodydata(expectedresponsebody, actualresponsebody):
    """Compares response in detail """
    pass

