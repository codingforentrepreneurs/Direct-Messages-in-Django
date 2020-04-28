from django.contrib.auth import get_user_model
from django.test import TestCase


from .models import Channel, ChannelMessage, ChannelUser

User = get_user_model()

class ChannelLookupTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create(username='cfe', password='learnforever')
        self.user_b = User.objects.create(username='ned_stark', password='winter_is_coming')
        self.user_c = User.objects.create(username='jon_snow', password='idontwantit')

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 3)
    
    def test_single_user_channel(self):
        qs = User.objects.all()
        for user in qs:
            channel_obj = Channel.objects.create()
            channel_obj.users.add(user)
        channel_qs = Channel.objects.all()
        self.assertEqual(channel_qs.count(), 3)
        channel_qs_1 = channel_qs.only_one()
        self.assertEqual(channel_qs_1.count(), channel_qs.count())

    def test_dual_user_channel(self):
        channel_obj = Channel.objects.create()
        ChannelUser.objects.create(user=self.user_a, channel=channel_obj)
        ChannelUser.objects.create(user=self.user_b, channel=channel_obj)
        channel_obj2 = Channel.objects.create()
        ChannelUser.objects.create(user=self.user_c, channel=channel_obj2)
        qs = Channel.objects.all()
        self.assertEqual(qs.count(), 2)
        with_two = qs.only_two()
        self.assertEqual(with_two.count(), 1)
