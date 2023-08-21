# import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings

client = Client(settings.SMS_AUTH["ACCOUNT_SID"], settings.SMS_AUTH["AUTH_TOKEN"])
verify = client.verify.services(settings.SMS_AUTH["VERIFY_SID"])


def sendSms(phone):
    verify.verifications.create(to=phone, channel="sms")


def checkSmsCode(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        return False
    return result.status == "approved"
