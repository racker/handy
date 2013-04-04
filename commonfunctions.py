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

    req_json = '{"auth":{"passwordCredentials":{"username":"marconidev","password":"2AITRDkvI2nt"}}}'
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

validttl = random.randint(60, 1209600)
negativettl = -validttl
invalidlongttl = random.randint(1209600, 120960012096001209600)

with open('/usr/share/dict/words', 'rt') as f:
    words = f.readlines()
words = [ w.rstrip() for w in words ]

def generatedict(dictlength):
    """Returns  dictionary of specified length. Key : Value will be random"""
    dict = {}
    while len(dict) < dictlength:
        key,value =  random.sample(words,2)
        dict.update({key:value})
    return dict

def singlemessagebody(**kwargs):
    """Returns message body for one message"""
    if "messagesize" in kwargs.keys():
        body = generatedict(kwargs["messagesize"])
    else:
        body = generatedict(2)
    if "ttl" in kwargs.keys():
        ttl = kwargs["ttl"]
    else:
        ttl = validttl
    messagebody = {"ttl":ttl, "body":body}
    return messagebody

def getmessagebody(**kwargs):
    """Returns message body to post"""
    messagecount = kwargs["messagecount"]
    bigmessagebody = []
    i = 0
    while i < messagecount:
        messagebody = singlemessagebody(**kwargs)
        bigmessagebody.append(messagebody)
        i = i + 1
    return bigmessagebody

def dummygetmessagebody(dict):
    """Dummy function to call getmessagebody because Robot framework does not
       support **kwargs"""
    dict = getmessagebody(**dict)
    return dict

def extractid(type, str):
    """Extracts the message ids returned by the server
       type can be /messages/ or /claims/ """
    id = str.partition(type)[2]
    id = id.rsplit(",")
    return id

def extractmsgid(responseheader):
    """Extracts message ID from the header returned for post message"""
    location = responseheader["location"]
    msgid = extractid("/messages/", location)
    return msgid

def verifymetadata(getdata, postedbody):
    """@todo - Really verify the metadata"""
    testresultflag = False
    getdata = str(getdata)
    postedbody = str(postedbody)
    print(getdata,type(getdata))
    print(postedbody,type(postedbody))
    if getdata in postedbody:
        print("AYYY")
    else:
        print("NAYYY")


def createurl(base_url,*msgidlist):
    """Creates url for retrieving messages with message id"""
    url = [(base_url + msgid) for msgid in msgidlist ]
    return url

def createurlfromhref(href):
    nexturl = BASE_SERVER + href
    return(nexturl)

def verifymsglength(count=10, *msglist):
    """Verifies the number of messages returned"""
    testresultflag = False
    msgbody = json.loads(msglist[0])
    msglist = msgbody["messages"]
    msgcount = len(msglist)
    if (msgcount <= count):
        testresultflag = True
    else:
        assert testresultflag, "Number of messages returned {}".format(msgcount)

def gethref( *msglist):
    """Verifies the links returned"""
    testresultflag = False
    msgbody = json.loads(msglist[0])
    link = msgbody["links"]
    href = link[0]["href"]
    return href


