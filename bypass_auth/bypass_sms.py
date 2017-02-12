"""
demo.py

flowroute-messaging-python is a Python SDK that provides methods to send an outbound SMS from a Flowroute phone number
and also to retrieve a Message Detail Record (MDR). These methods use v2 (version 2) of the Flowroute API.

Copyright Flowroute, Inc.  2016

"""
from random import randint
import configuration
from bypass_auth.FlowrouteMessagingLib.Controllers.APIController import *
from bypass_auth.FlowrouteMessagingLib.Models.Message import *

import pprint

# Set up your API credentials
username = configuration.USERNAME
password = configuration.PASSWORD
from_number = configuration.from_number

def send_auth(to_number,number_length = 4):
	#generate pass code
	numbers = [randint(0, 9) for _ in range(number_length)]
	msg = ''
	for x in numbers:
		msg += str(x)

	put_msg(msg,to_number)
	return numbers

# Create the Controller
def put_msg(message_content, to_number):
	controller = APIController(username=username, password=password)
	pprint.pprint(controller)

	# Build your message
	message = Message(to=to_number, from_=from_number, content=message_content)

	# Send your message
	try:
	    response = controller.create_message(message)
	    pprint.pprint(response)
	except APIException as e:
	    print("Error - " + str(e.response_code) + '\n')
	    pprint.pprint(e.response_body['errors'])
	    raise SystemExit        # can't continue from here

	# Get the MDR id from the response
	mdr_id = response['data']['id']

	# Retrieve the MDR record
	try:
	    mdr_record = controller.get_message_lookup(mdr_id)  # 'mdr1-b334f89df8de4f8fa7ce377e06090a2e'
	    pprint.pprint(mdr_record)
	except APIException as e:
	    print("Error - " + str(e.response_code) + '\n')
	    pprint.pprint(e.response_body['errors'])

if __name__ == '__main__':
	numbers = [randint(0, 9) for _ in range(4)]
	msg = ''
	for x in numbers:
		msg += str(x)
	put_msg(msg,'16508642215')
