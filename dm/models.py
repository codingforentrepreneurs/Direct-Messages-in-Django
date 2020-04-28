import uuid
from django.conf import settings
from django.db import models

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


class Message(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

# class Channel(BaseModel): # models.model