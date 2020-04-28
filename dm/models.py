import uuid
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
    def only_two(self):
        return self.annotate(num_users=Count("users")).filter(num_user=2)

class ChannelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ChannelQuerySet(self.model, using=self._db)


class Channel(BaseModel): # models.model
    # slack-like
    # 1 user
    # 2 users
    # 2+ users
    users = models.ManyToManyField(User, blank=True, through=ChannelUser)

    objects = ChannelManager()
