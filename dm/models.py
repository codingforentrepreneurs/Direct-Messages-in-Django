import uuid
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Count

User = settings.AUTH_USER_MODEL

# Create your models here.
class BaseModel(models.Model):
    # 1, 2, 3, 4, 5, 6
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # foreignkey
    # textfield

    class Meta:
        abstract = True


class ChannelMessage(BaseModel):
    channel = models.ForeignKey("Channel", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class ChannelUser(BaseModel):
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # permissions? 

# jon_snow -> ned_stark
# ned_stark -> jon_snow

# oursite.com/dm/jon_snow
# oursite.com/dm/ned_stark

class ChannelQuerySet(models.QuerySet):
    def only_one(self):
        return self.annotate(num_users=Count("users")).filter(num_users=1)

    def only_two(self):
        return self.annotate(num_users=Count("users")).filter(num_users=2)
    
    def filter_by_username(self, username):
        return self.filter(channeluser__user__username=username)

class ChannelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ChannelQuerySet(self.model, using=self._db)
    
    def filter_by_private_message(self, username_a, username_b):
        return self.get_queryset().only_two().filter_by_username(username_a).filter_by_username(username_b).order_by("timestamp")
    
    def get_or_create_current_user_private_message(self, user):
        qs = self.get_queryset().only_one().filter_by_username(user.username)
        if qs.exists():
            return qs.order_by("timestamp").first(), False
        channel_obj = Channel.objects.create()
        ChannelUser.objects.create(user=user, channel=channel_obj)
        return channel_obj, True


    def get_or_create_private_message(self, username_a, username_b):
        qs = self.filter_by_private_message(username_a, username_b)
        if qs.exists():
            return qs.order_by("timestamp").first(), False # obj, created
        User = apps.get_model("auth", model_name='User')
        user_a, user_b = None, None
        try:
            user_a = User.objects.get(username=username_a)
        except User.DoesNotExist:
            return None, False
        try:
            user_b = User.objects.get(username=username_b)
        except User.DoesNotExist:
            return None, False
        if user_a == None or user_b == None:
            return None, False
        channel_obj = Channel.objects.create()
        ch_u_a = ChannelUser(user=user_a, channel=channel_obj)
        ch_u_b = ChannelUser(user=user_b, channel=channel_obj)
        ChannelUser.objects.bulk_create([ch_u_a, ch_u_b])
        return channel_obj, True


class Channel(BaseModel): # models.model
    # slack-like
    # 1 user
    # 2 users
    # 2+ users
    users = models.ManyToManyField(User, blank=True, through=ChannelUser)
    # channel_type 
    # max_users 
    # status -> private, public
    # slug -> Lookup slug 
    # title -> Channel name/title

    objects = ChannelManager()

    class Meta:
        ordering = ['timestamp']
