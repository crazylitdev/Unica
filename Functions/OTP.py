from twilio.rest import Client
import random
import string

class OTP:

    def __init__(self) -> None:
        self.accountSid = "ACf01fafb0c16a1de381ab99cf5106aeaf"
        self.authToken = "bb4a73114fe2b03a7e11064a8fda80d8"
        self.client = Client(self.accountSid, self.authToken)
        self.number = "+17853845780"

    def sendOTP(self, phone:int) -> int:
        otp= "".join(random.choices(string.digits, k = 6))
        body = f"Your One Time Passcode (OTP) is {otp}. Please don't share this with anyone."
        self.client.messages.create(body=body, from_=self.number, to=string(phone))
        return otp
