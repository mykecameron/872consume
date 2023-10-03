import os
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


def index(request):
    SECRET = os.environ['SECRET']
    return HttpResponse(f"Hello, world. You're at the hotline index. The secret is {SECRET}")