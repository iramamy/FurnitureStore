from django.utils.crypto import get_random_string
from .models import Room


def chat_context(request):

    if request.user.is_authenticated:
        # authenticated user
        username = request.user.username
        room_name = f'u{username}'
        if 'room_name' not in request.session or request.session['room_name'] != room_name:
            request.session['room_name'] = room_name
            request.session['username'] = username

            Room.objects.get_or_create(room_name=room_name)
    else:
        # For guest
        username = get_random_string(6)
        room_name = f'g{username}'
        if 'room_name' not in request.session:
            request.session['room_name'] = room_name
            request.session['username'] = username

            Room.objects.get_or_create(room_name=room_name)
        else:
            username = request.session['username']
            room_name = request.session['room_name']

    request.room_name = room_name
    request.username = username
    
    return {
        'chat_room_name': room_name,
        'chat_username': username,
    }
