Have APIs to test?
"Have no fear, Handy is here!!!"
 
Handy is the API test suite for Marconi- using the Robot framework.
Handy is designed to make it easy to add new test cases as you have new end points. 


To Run the tests :

Make sure you have the following Python modules installed

    Requests
    
    Robot

    ConfigParser
  
cd to the handy directory

Update env.py to point to the env you want to run the tests against

Enter the cloud username & password in commonfunctions.py.getkeystonetoken()

To run tests use the pybot command in the following format,

     pybot queue/queue_tests.txt
     
     pybot messages/messages_tests.txt
     
     pybot claim/claim_tests.txt
