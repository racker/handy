import json
import http

import common

def initialize_test_suite(msgcount):
    pass


def verify_claim_msg(count, *claim_response):
    """
    Verifies claim messages. Validation steps include - verifying  the
    1. number of messages returned is <= limit specified
    2. query claim & verifying the response
    :param count: limit specified in the claim request
    :param claim_response : response returned for the claim request
    """
    msg_length_flag = False

    headers = claim_response[0]
    body = claim_response[1]

    msg_length_flag = verify_claim_msglength(count, body)
    if msg_length_flag :
        query_claim(headers, body)
    else:
        assert msg_length_flag, " More messages returned than specified in limit"


def verify_claim_msglength(count, *body):
    """ Validates that number of messages returned is <= limit specified """
    msg_list = body
    msg_list = json.loads(msg_list[0])
    return (len(msg_list) <= count)


def query_claim(headers, *body):
    """
    Performs a Query Claim using the href in post claim
    Compares the messages returned in Query claim with the messages
    returned on Post Claim
    """
    test_result_flag = False

    msg_list = body[0]
    msg_list = json.loads(msg_list)

    location = headers["Location"]
    url = common.functionlib.create_url_from_appender(location)
    header = common.functionlib.create_marconi_headers()

    get_msg = http.get(url, header)
    if get_msg.status_code == 200:
        query_body = json.loads(get_msg.text)
        query_msgs = query_body["messages"]
        test_result_flag = verify_query_msgs(query_msgs, msg_list)

    if test_result_flag:
        return test_result_flag
    else:
        print "URL"
        print url
        print "HEADER"
        print header
        print "Messages returned by Query Claim"
        print querymsgs
        print "# of Messages returned by Query Claim", len(querymsgs)
        print 'Messages returned by Claim Messages'
        print msg_list
        print "# of Messages returned by Claim messages", len(msg_list)
        assert test_result_flag, "Query Claim Failed"


def verify_query_msgs(querymsgs, msg_list):
    """
    Compares the messages returned in Query Claim with the messages
    returned when the claim was posted
    """
    test_result_flag = True
    idx = 0

    for msg in querymsgs:
        if ((msg["body"] != msg_list[idx]["body"]) or
            (msg["href"] != msg_list[idx]["href"]) or
            (msg["ttl"] != msg_list[idx]["ttl"])):
               test_result_flag = False
        idx = idx + 1

    return test_result_flag


def patch_claim(*claim_response):
    """
    Extracts claim id from the POST response input & updates the claim.
    If PATCH claim succeeds, verifies that the claim TTL is extended
    """
    test_result_flag = False

    headers = claim_response[0]
    location = headers["Location"]
    url = common.functionlib.create_url_from_appender(location)
    header = common.functionlib.create_marconi_headers()

    body = claim_response[1]

    ttl_value = 300
    payload = '{ "ttl": ttlvalue }'
    payload = payload.replace("ttlvalue", str(ttl_value))

    patch_response = http.patch(url, header, body = payload)
    if patch_response.status_code == 204 :
        test_result_flag = verify_patch_claim(url, header, ttl_value)
    else:
        print "Patch HTTP Response code: {}".format(patch_response.status_code)
        print patch_response.headers
        print patch_response.text
        assert test_result_flag, "Patch Claim Failed"

    if not test_result_flag:
        assert test_result_flag, "Query claim after the patch failed"


def verify_patch_claim(url, header, ttl_extended):
    """
    Verifies if patch claim was successful, by
    1. Getting the claim
    2. Checking tht the actual claim TTL value is > TTL in the patch request
    :param ttl_extended : TTL posted in the patch request
    """
    test_result_flag = True

    get_claim = http.get(url,header)
    response_body = json.loads(get_claim.text)

    ttl = response_body["ttl"]
    if ttl < ttl_extended:
        print get_claim.status_code
        print get_claim.headers
        print get_claim.text
        test_result_flag = False

    return test_result_flag


def create_urllist_fromhref(*response):
    """
    Return a url list by extracting all the hrefs
    :param *response : http response text with the list of messages
    """
    rspbody = json.loads(response[1])
    urllist = [common.functionlib.create_url_from_appender(item["href"])
               for item in rspbody]
    return urllist


def delete_claimed_msgs(*claim_response):
    """
    Deletes claimed messages.
    Verifies that the deletes were successful by doing a GET on the deleted msg
    """
    test_result_flag = False

    urllist = create_urllist_fromhref(*claim_response)
    header = common.functionlib.create_marconi_headers()

    for url in urllist:
        delete_response = http.delete(url,header)
        if delete_response.status_code == 204:
            print url
            get_deleted = http.get(url,header)
            if get_deleted.status_code == 404:
                test_result_flag = True
            else:
                print "GET deleted message: {}".format(url)
                print get_deleted.status_code
                print get_deleted.headers
                print get_deleted.text
        else:
            print "DELETE message with claim ID: {}".format(url)
            print delete_response.status_code
            print delete_response.headers
            print delete_response.text

    if not test_result_flag:
        assert test_result_flag, "DELETE message with claim ID failed"




