from django.contrib import admin
from .models import Room, Message

class MessageInline(admin.TabularInline):
    model = Message
    readonly_fields = ['room', 'sender', 'message']
    extra = 0

class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ['room_name',]
    inlines = [MessageInline]

admin.site.register(Room, RoomAdmin)
admin.site.register(Message)
