from messages import msgfnlib
import json

def initializetestsuite(msgcount):
    pass

def verifyclaimmsg(count, *postresponse):
    msglengthflag = False
    headers = postresponse[0]
    body = postresponse[1]
    msglengthflag = verifyclaimsglength(count, body)
    print "msglengthflag", msglengthflag


def verifyclaimsglength(count, *body):
    msglist = body
    msglist = json.loads(msglist[0])
    return (len(msglist) <= count)

