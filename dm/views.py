from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.views.generic import DetailView
from django.shortcuts import render

from .models import Channel

class PrivateMessageDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dm/private_message.html'
    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        my_username = self.request.user.username
        channel_obj, _ = Channel.objects.get_or_create_private_message(my_username, username)
        if channel_obj == None:
            raise Http404
        return channel_obj

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