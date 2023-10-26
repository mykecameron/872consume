import os
from django.shortcuts import render
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Gather
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import openai

openai.api_key = os.environ['OPENAI_KEY']

def index(request):
    """Get a voice call"""

    resp = VoiceResponse()

    # Listen to what the caller says
    gather = Gather(input="speech", action="/hotline/gather", method="POST") 
    
    # Read a message aloud to the caller
    gather.say(
        __chatGptResponse(), 
        'Polly.Joey',
    )

    resp.append(gather)
    resp.say("You didn't say anything!")
    
    print("Responding")
    return HttpResponse(resp,  content_type='text/xml')

# TODO: make this validate that the request is coming from Twilio
@require_POST
@csrf_exempt
def gather(request):
    print(request.headers)
    speechResult = request.POST.get('SpeechResult')
    print(speechResult)
    resp = VoiceResponse()
    resp.say(__chatGptResponse(speechResult))
    
    return HttpResponse(resp,  content_type='text/xml')
    
def __chatGptResponse(message="Hello?"):
    print("Asking chat gpt...")
    prompt = "You are a deceptive and somewhat incompetent sales representative named Joey who works for Consumer LLC, a corporation specializing in providing 'Full Life Consolidation' services for their clients. You are on a call from a potential client. Respond with an appropriate, brief response."

    conversation = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    modelReply = response['choices'][0]['message']['content']

    print(f"Chat GPT says: {modelReply}")
    return modelReply
