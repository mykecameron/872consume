import os
from django.shortcuts import render
from twilio.rest import Client as TwilioClient

# Create your views here.


from django.http import HttpResponse


def index(request):
    twilio_sid = os.environ['TWILIO_SID']
    twilio_token = os.environ['TWILIO_AUTH_TOKEN']

    client = TwilioClient(twilio_sid, twilio_token)

    message = client.messages.create(
        to="+17745730274",
        from_="+18722667863",
        body="Hello from the hotline app")

    return HttpResponse(f"A message has been sent! SID: {message.sid}")