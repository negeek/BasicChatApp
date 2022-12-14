from audioop import maxpp
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.thread_name


class Group(models.Model):
    avatar = models.FileField(
        default='default.jpg', upload_to='profile_images/')
    group_name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        get_user_model(), related_name='group_members')
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.group_name


class GroupChat(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.thread_name


class DeletedMessages(models.Model):
    username = models.CharField(max_length=100)
    thread_name = models.CharField(max_length=50)
    message_id = models.IntegerField()

    def __str__(self):
        return f'{self.message_id}'
