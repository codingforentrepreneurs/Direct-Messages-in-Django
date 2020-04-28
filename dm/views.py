from django.http import HttpResponse

from django.shortcuts import render

from .models import Channel

# Create your views here.
def private_message_view(request, username, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponse("Nope..")
    my_username = request.user.username
    channel_obj, created = Channel.objects.get_or_create_private_message(my_username, username)
    if created:
        print("yes it was")
    channel_users = channel_obj.channeluser_set.all().values("user__username")
    print(channel_users)
    channel_messages = channel_obj.channelmessage_set.all()
    print(channel_messages.values("content"))
    return HttpResponse(f"channel items - {channel_obj.id}")