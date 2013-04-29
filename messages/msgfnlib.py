from __future__ import with_statement
import json
import random

import common
import http

validttl = random.randint(60, 1209600)
negativettl = -validttl
invalidlongttl = random.randint(1209600, 120960012096001209600)

with open('/usr/share/dict/words', 'rt') as f:
    words = f.readlines()
words = [ w.rstrip() for w in words ]


def generate_dict(dictlength):
    """Returns  dictionary of specified length. Key : Value will be random"""
    dict = {}
    while len(dict) < dictlength:
        key, value =  random.sample(words,2)
        dict.update({key:value})
    return dict


def single_message_body(**kwargs):
    """Returns message body for one message"""
    if "messagesize" in kwargs.keys():
        body = generate_dict(kwargs["messagesize"])
    else:
        body = generate_dict(2)
    if "ttl" in kwargs.keys():
        ttl = kwargs["ttl"]
    else:
        ttl = validttl
    messagebody = {"ttl":ttl, "body":body}
    return messagebody


def get_message_body(**kwargs):
    """Returns message body to post"""
    messagecount = kwargs["messagecount"]
    bigmessagebody = []
    i = 0
    while i < messagecount:
        messagebody = single_message_body(**kwargs)
        bigmessagebody.append(messagebody)
        i = i + 1
    return bigmessagebody


def dummyget_message_body(dict):
    """Dummy function to call get_message_body because Robot framework does not
       support **kwargs"""
    dict = get_message_body(**dict)
    return dict


def extract_id(type, str):
    """Extracts the message ids returned by the server
       type can be /messages/ or /claims/ """
    id = str.partition(type)[2]
    id = id.rsplit(",")
    return id


def extract_msg_id(responseheader):
    """Extracts message ID from the header returned for post message"""
    location = responseheader["location"]
    msgid = extract_id("/messages/", location)
    return msgid


def verify_metadata(getdata, postedbody):
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


def create_url(base_url, *msgidlist):
    """Creates url for retrieving messages with message id"""
    url = [(base_url + msgid) for msgid in msgidlist ]
    return url


def verify_msg_length(count=10, *msglist):
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


def get_href( *msglist):
    """Verifies the links returned"""
    msgbody = json.loads(msglist[0])
    link = msgbody["links"]
    href = link[0]["href"]
    return href


def verify_post_msg(msgheaders, postedbody):
    """Verifies the response of POST Message(s) - Retrieves the posted
       Message(s) & validates the message metadata"""
    testresultflag = False
    location = msgheaders['location']
    url = common.commonfunctions.create_url_from_appender(location)
    header = common.commonfunctions.create_marconi_headers()
    getmsg = http.get(url, header)
    if getmsg.status_code == 200:
        testresultflag = verify_metadata(getmsg.text, postedbody)
    else:
        print("Failed to GET {}".format(url))
        print("Request Header")
        print header
        print("Response Headers")
        print getmsg.headers
        print("Response Body")
        print getmsg.text
        assert testresultflag, "HTTP Response code {}".format(getmsg.status_code)


def get_next_msgset(responsetext):
    """Follows the href path & GETs the next batch of messages recursively"""
    testresultflag = False
    href = get_href(responsetext)
    url = common.commonfunctions.create_url_from_appender(href)
    header = common.commonfunctions.create_marconi_headers()
    getmsg = http.get(url, header)
    if getmsg.status_code == 200:
        return get_next_msgset(getmsg.text)
    elif getmsg.status_code == 204:
        testresultflag = True
        return testresultflag
    else:
        testresultflag = False
        print("Failed to GET {}".format(url))
        print(getmsg.text)
        assert testresultflag, "HTTP Response code {}".format(getmsg.status_code)


def verify_get_msgs(count, *getresponse):
    #import pdb; pdb.set_trace()
    """Verifies GET message & does a recursive GET if needed"""
    testresultflag = False
    headers = getresponse[0]
    body = getresponse[1]
    msglengthflag = verify_msg_length(count,body)
    if msglengthflag:
        testresultflag = get_next_msgset(body)
    else:
        print("Messages returned exceed requested number of messages")
        testresultflag = False
    if not testresultflag:
        assert testresultflag, "Recursive Get Messages Failed"


def verify_delete(url, header):
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


def delete_msg(*postresponse):
    """Post DELETE message & verifies that a subsequent GET returns 404"""
    testresultflag = False
    headers = str(postresponse[0])
    headers = headers.replace("'",'"')
    headers = json.loads(headers)
    location = headers['location']
    url = common.commonfunctions.create_url_from_appender(location)
    header = common.commonfunctions.create_marconi_headers()
    deletemsg = http.delete(url, header)
    if deletemsg.status_code == 204 :
        testresultflag = verify_delete(url,header)
    else:
        print("DELETE message failed")
        print("URL")
        print url
        print("headers")
        print header
        print("Response Body")
        print deletemsg.text
        assert testresultflag, "DELETE Response Code {}".format(deletemsg.status_code)
