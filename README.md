Have APIs to test? - "Have no fear, Handy is here!!!"
 
Handy is the API test suite for Marconi- using the Robot framework.
Handy is designed to make it easy to add new test cases as you have new end points. 


To Run the tests :

Make sure you have the following Python modules installed

    Requests
    
    Robot

    ConfigParser
  
cd to the handy directory

Update etc/handy.conf to point to the env you want to run the tests against

Enter the cloud username & password in  etc/handy.conf

To run tests use the pybot command in the following format,

     pybot queue/queue_tests.txt
     
     pybot messages/messages_tests.txt
     
     pybot claim/claim_tests.txt

To Add new tests :

1. Add test case definition in the robot test case file (queue/queue_tests.txt, messages/messages_tests.txt, claim/claim_tests.txt)
   Refer http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#creating-test-cases

2. Add test data in test_data.csv of your test directory (eg. queue/queue_tests.txt)

3. Add any validation logic you might need to either,
   the corresponing *fnlib.py (eg queue/queuefnlib.py). (OR)
   common/functionlib.py  (If the code can be used across multiple functionalities)
