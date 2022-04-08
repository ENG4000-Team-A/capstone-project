import os

from twilio.rest import Client
from twilio.base import exceptions

NOTIF_TIMES = [
    60 * 5,  # 5 mins
    60 * 15,  # 15 mins
]
# country code for Canada and US, will need proper way to get for other countries
COUNTRY_CODE = "+1"

account_sid = os.environ.get('TWILIO_ACCOUNT_SID', "empty")
auth_token = os.environ.get('TWILIO_AUTH_TOKEN', "empty")
from_number = ''

client = Client(account_sid, auth_token)

try:
    phone_number_list = client.incoming_phone_numbers.list(limit=1)
    from_number = phone_number_list[0].phone_number
except exceptions.TwilioException:
    NOTIF_TIMES = []
    print("Twilio credentials invalid. Disabling notifications")
except:
    NOTIF_TIMES = []
    print("no phone numbers in twilio account. Disabling notifications")


def sendSMS(phone_number: str, msg: str):
    """
	Sends a SMS message to phoneNumber
	phoneNumber must include dialing code
	eg '+14161231234'
	"""
    message = client.messages.create(
        body=msg,
        from_=from_number,
        to=COUNTRY_CODE + phone_number
    )
