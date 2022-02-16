import os
from twilio.rest import Client

NOTIF_TIMES = 	[
				60*5, # 5 mins
				60*15, # 15 mins
				]

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_number = ''

client = Client(account_sid, auth_token)

phone_number_list = client.incoming_phone_numbers.list(limit=1)
try:
	from_number = phone_number_list[0].phone_number
except :
	print("no phone numbers in twilio account")



def sendSMS(phone_number: str, msg: str):
	"""
	Sends a SMS message to phoneNumber
	phoneNumber must include dialing code
	eg '+14161231234'
	"""
	message = client.messages.create(
			body=msg,
			from_=from_number,
			to=phone_number
		)
