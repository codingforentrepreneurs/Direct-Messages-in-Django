from django.http import HttpResponse

from django.shortcuts import render

from .models import Channel

# Create your views here.
def private_message_view(request, username, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponse("Nope..")
    my_username = request.user.username
    qs = Channel.objects.filter_by_private_message(my_username, username)
    if qs.exists():
        channel_obj = qs.first()
        channel_users = channel_obj.channeluser_set.all().values("user__username")
        print(channel_users)
        channel_messages = channel_obj.channelmessage_set.all()
        print(channel_messages.values("content"))
    return HttpResponse(f"channel items - {qs.count()}")