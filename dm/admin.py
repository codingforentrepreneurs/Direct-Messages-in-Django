from django.contrib import admin

from .models import Channel, ChannelMessage, ChannelUser

class ChannelMessageInline(admin.TabularInline):
    model = ChannelMessage
    extra = 1

class ChannelUserInline(admin.TabularInline):
    model = ChannelUser
    extra = 1

class ChannelAdmin(admin.ModelAdmin):
    inlines = [ChannelUserInline, ChannelMessageInline]
    class Meta:
        model = Channel

admin.site.register(Channel, ChannelAdmin)



admin.site.register(ChannelMessage)