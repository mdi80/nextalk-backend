import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
verified_number = "+989302362393"
client = Client(account_sid, auth_token)


# verification = client.verify.v2.services(verify_sid).verifications.create(
#     to="+989302362393", channel="sms"
# )


otp_code = input("Please enter the OTP:")

verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
    to=verified_number, code=otp_code
)


print(verification_check.status)
