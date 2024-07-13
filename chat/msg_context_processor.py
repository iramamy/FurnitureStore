from .models import Room, Message

def room_message(request):
    room_name = request.session.get('room_name')
    print('Room name', room_name)

    if room_name:
        room, _ = Room.objects.get_or_create(room_name=room_name)
        get_messages = Message.objects.filter(room=room)
    else:
        get_messages = ['hello']

    return {
        'get_messages': get_messages,
    }
