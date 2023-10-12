from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("incoming", views.incoming, name="incoming"),
]