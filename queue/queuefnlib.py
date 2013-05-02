import binascii
import json
import os

import common


def verify_queue_stats(*get_response):
    """
    Verifies that
       1. stats json body has the keys - action & messages
       2. messages json has the keys - claimed & free
       3. claimed & free key values are int
    """

    test_result_flag = True
    headers = get_response[0]
    body = json.loads(get_response[1])

    keys_in_body = body.keys()
    keys_in_body.sort()

    if  (keys_in_body == ["actions", "messages"]):
        stats = body["messages"]
        keys_in_stats = stats.keys()
        keys_in_stats.sort()
        if (keys_in_stats == ["claimed", "free"]) :
            try:
                int(stats["claimed"])
                int(stats["free"])
            except:
                test_result_flag = False
        else:
            test_result_flag = False
    else:
        test_result_flag = False

    if test_result_flag:
        return test_result_flag
    else:
        print headers
        print body
        assert test_result_flag, "Get Request stats failed"


def get_queue_name(namelength = 513):
    """
    Returns a queuename of specified length.
    By default, a name longer than Marconi allows - currently 512 bytes
    """

    appender = "/queues/" + binascii.b2a_hex(os.urandom(namelength))
    url = common.functionlib.create_url_from_appender(appender)
    return url


def queue_teardown():
    pass
