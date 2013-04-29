import json
import binascii
import os
import common


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

def verifyqueuestats(*getresponse):
    """Verifies that
       1. stats json body has the keys - action & messages
       2. messages json has the keys - claimed & free
       3. claimed & free key values are int """
    testresultflag = True
    headers = getresponse[0]
    body = json.loads(getresponse[1])
    keysinbody = body.keys()
    keysinbody.sort()
    if  (keysinbody == ["actions", "messages"]):
        stats = body["messages"]
        keysinstats = stats.keys()
        keysinstats.sort()
        if (keysinstats == ["claimed", "free"]) :
            try:
                int(stats["claimed"])
                int(stats["free"])
            except:
                testresultflag = False
        else:
            testresultflag = False
    else:
        testresultflag = False
    if testresultflag:
        return testresultflag
    else:
        print headers
        print body
        assert testresultflag, "Get Request stats failed"

def getqueuename(namelength = 513):
    """Returns a queuename of specified length.
       By default, a name longer than Marconi allows - currently 512 bytes"""
    appender = "/queues/" + binascii.b2a_hex(os.urandom(namelength))
    url = common.commonfunctions.createurlfromappender(appender)
    return url

def queueteardown():
    pass
