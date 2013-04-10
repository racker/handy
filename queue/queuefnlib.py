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