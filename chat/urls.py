from django.urls import path
from . import views

urlpatterns = [
    path(
        '<str:room_name>/<str:username>/',
        views.room_chat,
        name='room_chat'),
]