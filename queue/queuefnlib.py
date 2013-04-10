import json

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
    testresultflag = True
    headers = getresponse[0]
    body = json.loads(getresponse[1])
    keysinbody = body.keys()
    keysinbody.sort()
    if  (keysinbody == ["actions", "messages"]):
        stats = body["messages"]
        keysinstats = stats.keys()
        keysinstats.sort()
        if (keysinstats == ["claimed", "expired", "total"]) :
            try:
                int(stats["claimed"])
                int(stats["expired"])
                int(stats["total"])
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