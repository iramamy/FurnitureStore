from django.shortcuts import render
from .models import Room, Message

def room_chat(request, room_name, username):

    existing_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(
        room=existing_room
    )

    context = {
        'messages': get_messages,
    }

    return render(request, 'includes/chat.html', context)
