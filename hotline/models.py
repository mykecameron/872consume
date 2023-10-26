from django.db import models

class Call(models.Model):
    call_sid = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    content = models.TextField()
    role = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
