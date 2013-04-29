#from messages import msgfnlib
import json
import http
import common

def initializetestsuite(msgcount):
    pass

def createurlfromlocn(location):
    url = str(common.config.BASE_SERVER + location)
    return(url)

def verifyclaimmsg(count, *postresponse):
    """Verifies claim messages. Validation steps include - verifying  the"""
    """1. number of messages returned is <= limit specified  """
    """2. query claim & verifying the response"""
    msglengthflag = False
    headers = postresponse[0]
    body = postresponse[1]
    msglengthflag = verifyclaimsglength(count, body)
    if msglengthflag :
        queryclaim(headers, body)
    else:
        assert msglengthflag, " More messages returned than specified in limit"


def verifyclaimsglength(count, *body):
    """ Validates that number of messages returned is <= limit specified """
    msglist = body
    msglist = json.loads(msglist[0])
    return (len(msglist) <= count)


def queryclaim(headers, *body):
    """ Performs a Query Claim using the href in post claim
        Compares the messages returned in Query claim with the messages
        returned on Post Claim"""
    testresultflag = False
    msglist = body[0]
    msglist = json.loads(msglist)
    location = headers["Location"]
    url = createurlfromlocn(location)
    header = common.commonfunctions.createmarconiheaders()
    getmsg = http.get(url,header)
    if getmsg.status_code == 200:
        querybody = json.loads(getmsg.text)
        querymsgs = querybody["messages"]
        testresultflag = verifyquerymsgs(querymsgs, msglist)
    if testresultflag:
        return testresultflag
    else:
        print "URL"
        print url
        print "HEADER"
        print header
        print "Messages returned by Query Claim"
        print querymsgs
        print "# of Messages returned by Query Claim", len(querymsgs)
        print 'Messages returned by Claim Messages'
        print msglist
        print "# of Messages returned by Claim messages", len(msglist)
        assert testresultflag, "Query Claim Failed"

def verifyquerymsgs(querymsgs, msglist):
    """Compares the messages returned in Query Claim with the messages
       returned when the claim was posted"""
    testresultflag = True
    idx = 0
    for msg in querymsgs:
        if ((msg["body"] != msglist[idx]["body"]) or
            (msg["href"] != msglist[idx]["href"]) or
            (msg["ttl"] != msglist[idx]["ttl"])):
               testresultflag = False
        idx = idx + 1
    return testresultflag

def patchclaim(*postresponse):
    """Extracts claim id from the POST response input & update the claim """
    testresultflag = False
    headers = postresponse[0]
    body = postresponse[1]
    location = headers["Location"]
    url = createurlfromlocn(location)
    header = common.commonfunctions.createmarconiheaders()
    ttlvalue = 300
    payload = '{ "ttl": ttlvalue }'
    payload = payload.replace("ttlvalue", str(ttlvalue))
    print payload
    patchresponse = http.patch(url, header, body = payload)
    if patchresponse.status_code == 204 :
        testresultflag = verifypatchclaim(url, header, ttlvalue)
    else:
        print "Patch HTTP Response code: {}".format(patchresponse.status_code)
        print patchresponse.headers
        print patchresponse.text
        assert testresultflag, "Patch Claim Failed"
    if not testresultflag:
        assert testresultflag, "Query claim after the patch failed"


def verifypatchclaim(url, header, ttlvalue):
    testresultflag = True
    queryclaim = http.get(url,header)
    responsebody = json.loads(queryclaim.text)
    ttl = responsebody["ttl"]
    if ttl < ttlvalue:
        print queryclaim.status_code
        print queryclaim.headers
        print queryclaim.text
        testresultflag = False
    return testresultflag

def createurllistfromhref(*postresponse):
    rspbody = json.loads(postresponse[1])
    urllist = [createurlfromlocn(item["href"]) for item in rspbody]
    return urllist

def deleteclaimedmsgs(*postresponse):
    testresultflag = False
    urllist = createurllistfromhref(*postresponse)
    header = common.commonfunctions.createmarconiheaders()
    for url in urllist:
        deletersp = http.delete(url,header)
        if deletersp.status_code == 204:
            print url
            getdeleted = http.get(url,header)
            if getdeleted.status_code == 404:
                testresultflag = True
            else:
                print "GET deleted message: {}".format(url)
                print getdeleted.status_code
                print getdeleted.headers
                print getdeleted.text
        else:
            print "DELETE message with claim ID: {}".format(url)
            print deletersp.status_code
            print deletersp.headers
            print deletersp.text
    if not testresultflag:
        assert testresultflag, "DELETE message with claim ID failed"




