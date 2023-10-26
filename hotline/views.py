import os
import pprint
from django.shortcuts import render
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Gather
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import openai

from hotline.models import Call, Message

openai.api_key = os.environ['OPENAI_KEY']

def index(request):
    # Persist call
    call = Call.objects.create(
        call_sid=request.GET.get('CallSid'),
        phone_number=request.GET.get('Caller'),
    )

    # Generate and persist response
    chat_gpt_response = __chat_gpt_response(call)
    Message.objects.create(
        call=call,
        role="assistant",
        content=chat_gpt_response, 
    )

    # Respond
    resp = VoiceResponse()
    gather = Gather(input="speech", action="/hotline/gather", method="POST") 

    gather.say(chat_gpt_response, 'Polly.Joey')
    resp.append(gather)

    # Loop if no input
    resp.redirect('/hotline/')
    
    return HttpResponse(resp,  content_type='text/xml')

# TODO: make this validate that the request is coming from Twilio
@require_POST
@csrf_exempt
def gather(request):
    # Get response from caller
    speech_result = request.POST.get('SpeechResult')
    call = Call.objects.get(call_sid=request.POST.get('CallSid'))
    print(call)

    # Persist response from caller
    Message.objects.create(
        call=call,
        content=speech_result,
        role="user",
    )

    resp = VoiceResponse()
    gather = Gather(input="speech", action="/hotline/gather", method="POST") 

    # Generate and persist ChatGPT response
    chat_gpt_response = __chat_gpt_response(call)
    Message.objects.create(
        call=call,
        role="assistant",
        content=chat_gpt_response,
    )

    gather.say(chat_gpt_response, 'Polly.Joey')
    resp.append(gather)
    resp.redirect('/hotline/')
    
    return HttpResponse(resp,  content_type='text/xml')
    
def __chat_gpt_response(call):
    print("Asking chat gpt...")

    prompt = "You are a deceptive and somewhat incompetent sales representative named Joey who works for Consumer LLC, a corporation specializing in providing 'Full Life Consolidation' services for their clients. You are receiving a phone call from a potential client. Answer the call. Keep all your responses brief (a few sentences at most)."

    conversation = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Hello?"},
    ]

    messages = call.message_set.all()

    for message in messages:
        conversation.append({"role": message.role, "content": message.content})

    pprint.pp(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    modelReply = response['choices'][0]['message']['content']

    print(f"Chat GPT says: {modelReply}")
    return modelReply
