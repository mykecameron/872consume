import os
from django.shortcuts import render
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse
from django.http import HttpResponse
import openai

openai.api_key = os.environ['OPENAI_KEY']

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
    resp.say(__response(), 'Polly.Joey')

    return HttpResponse(resp)

def __response():
    prompt = "You are a deceptive and somewhat incompetent sales representative named Joey who works for Consumer LLC, a corporation specializing in providing 'Full Life Consolidation' services for their clients. You are answering a call from a potential client."
    user_input = "Hello?"

    conversation = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    model_reply = response['choices'][0]['message']['content']

    return model_reply
