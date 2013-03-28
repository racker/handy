import csv
import httpfnlib
import json

#START ENVIRONMENT VARIABLES
HOST = "marconi.test.com"
USERAGENT = "useragent"
AUTH_URL = "https://identity.api.rackspacecloud.com/v2.0/tokens"
RSE_SERVER = "rse.drivesrvr-qa.com"
MARCONI_SERVER = "166.78.150.92:8888"
#END ENVIRONMENT VARIABLES


#START TEST DATA
def getkeystonetoken():
    """Gets Keystone Auth token"""

    req_json = '{"auth":{"passwordCredentials":{"username":"","password":""}}}'
    header = '{"Host": "identity.api.rackspacecloud.com","Content-Type": "application/json","Accept": "application/json"}'
    url = AUTH_URL
    response = httpfnlib.httppost(url = url,header = header, body = req_json)
    responsebody = json.loads(response.text)
    authtoken = responsebody["access"]["token"]["id"]
    return authtoken

def createmarconiheaders(host,useragent):
    """Returns headers to be used for all Marconi requests"""

    authtoken = getkeystonetoken()
    headers = '{"Host": "<HOST>","User-Agent": "<USER-AGENT>","Date": "<DATE>",'
    headers += '"Accept": "application/json","Accept-Encoding": "gzip",'
    headers += '"X-Auth-Token": "<AuthToken>"}'
    headers = headers.replace("<AuthToken>", authtoken)
    headers = headers.replace("<HOST>", host)
    headers = headers.replace("<USER-AGENT>", useragent)
    return headers

def get_data(host, useragent):
    """Gets Test Data from a csv file"""

    DATA = []
    header = createmarconiheaders(host, useragent)
    with open('paralleltests/test_data.csv','rb') as datafile:
        testdata = csv.DictReader(datafile, delimiter = '|')
        for row in testdata:
            DATA.append(row)
    # Replacing header data to use Marconi specific headers
    # Replace the for loop below to implement project specific logic
    for row in DATA:
        row['header'] = header
        row['url'] = row['url'].replace("<SERVER>",MARCONI_SERVER)
    return DATA

API_TEST_DATA = get_data(HOST, USERAGENT)
#END TEST DATA
