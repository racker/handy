from __future__ import with_statement
import random
import json
from env import  *
import http
import common

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
        key, value =  random.sample(words,2)
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
    print(getdata, type(getdata))
    print(postedbody, type(postedbody))
    if getdata in postedbody:
        print("AYYY")
    else:
        print("NAYYY")


def createurl(base_url, *msgidlist):
    """Creates url for retrieving messages with message id"""
    url = [(base_url + msgid) for msgid in msgidlist ]
    return url


def verifymsglength(count=10, *msglist):
    """Verifies the number of messages returned"""
    testresultflag = False
    msgbody = json.loads(msglist[0])
    msglist = msgbody["messages"]
    msgcount = len(msglist)
    if (msgcount <= count):
        testresultflag = True
    else:
        return testresultflag
    return testresultflag

def gethref( *msglist):
    """Verifies the links returned"""
    msgbody = json.loads(msglist[0])
    link = msgbody["links"]
    href = link[0]["href"]
    return href

def verifypostmsg(msgheaders, postedbody):
    """Verifies the response of POST Message(s) - Retrieves the posted
       Message(s) & validates the message metadata"""
    testresultflag = False
    location = msgheaders['location']
    url = common.commonfunctions.createurlfromappender(location)
    header = common.commonfunctions.createmarconiheaders()
    getmsg = http.get(url, header)
    if getmsg.status_code == 200:
        testresultflag = verifymetadata(getmsg.text, postedbody)
    else:
        print("Failed to GET {}".format(url))
        print("Request Header")
        print header
        print("Response Headers")
        print getmsg.headers
        print("Response Body")
        print getmsg.text
        assert testresultflag, "HTTP Response code {}".format(getmsg.status_code)

def getnextmsgset(responsetext):
    """Follows the href path & GETs the next batch of messages recursively"""
    testresultflag = False
    href = gethref(responsetext)
    url = common.commonfunctions.createurlfromappender(href)
    header = common.commonfunctions.createmarconiheaders()
    getmsg = http.get(url, header)
    if getmsg.status_code == 200:
        return getnextmsgset(getmsg.text)
    elif getmsg.status_code == 204:
        testresultflag = True
        return testresultflag
    else:
        testresultflag = False
        print("Failed to GET {}".format(url))
        print(getmsg.text)
        assert testresultflag, "HTTP Response code {}".format(getmsg.status_code)

def verifygetmsgs(count, *getresponse):
    #import pdb; pdb.set_trace()
    """Verifies GET message & does a recursive GET if needed"""
    testresultflag = False
    headers = getresponse[0]
    body = getresponse[1]
    msglengthflag = verifymsglength(count,body)
    if msglengthflag:
        testresultflag = getnextmsgset(body)
    else:
        print("Messages returned exceed requested number of messages")
        testresultflag = False
    if not testresultflag:
        assert testresultflag, "Recursive Get Messages Failed"

def verifydelete(url, header):
    testresultflag = False
    getmsg = http.get(url, header)
    if getmsg.status_code == 404:
        testresultflag = True
    else:
        print("GET after DELETE failed")
        print("URL")
        print url
        print("headers")
        print header
        print("Response Body")
        print getmsg.text
        assert testresultflag, "GET Response Code {}".format(getmsg.status_code)
    return testresultflag

def deletemsg(*postresponse):
    """Post DELETE message & verifies that a subsequent GET returns 404"""
    testresultflag = False
    headers = str(postresponse[0])
    headers = headers.replace("'",'"')
    headers = json.loads(headers)
    location = headers['location']
    url = common.commonfunctions.createurlfromappender(location)
    header = common.commonfunctions.createmarconiheaders()
    deletemsg = http.delete(url, header)
    if deletemsg.status_code == 204 :
        testresultflag = verifydelete(url,header)
    else:
        print("DELETE message failed")
        print("URL")
        print url
        print("headers")
        print header
        print("Response Body")
        print deletemsg.text
        assert testresultflag, "DELETE Response Code {}".format(deletemsg.status_code)
