import os
from django.shortcuts import render
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse

from django.http import HttpResponse

def index(request):
    """Send a text"""

    twilio_sid = os.environ['TWILIO_SID']
    twilio_token = os.environ['TWILIO_AUTH_TOKEN']
    
    client = TwilioClient(twilio_sid, twilio_token)

    message = client.messages.create(
        to="+17745730274",
        from_="+18722667863",
        body="Hello from the hotline app")

    return HttpResponse(f"A message has been sent! SID: {message.sid}")

def incoming(request):
    """Get a voice call"""

    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Hello world!")

    return HttpResponse(resp)