import binascii
import json
import os

import common


def verify_metadata(getdata, postedbody):
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


def verify_queue_stats(*getresponse):
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


def get_queue_name(namelength = 513):
    """Returns a queuename of specified length.
       By default, a name longer than Marconi allows - currently 512 bytes"""
    appender = "/queues/" + binascii.b2a_hex(os.urandom(namelength))
    url = common.commonfunctions.create_url_from_appender(appender)
    return url


def queue_teardown():
    pass
