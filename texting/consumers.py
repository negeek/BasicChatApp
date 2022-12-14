from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import ChatModel, GroupChat
from django.shortcuts import get_object_or_404


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']

        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        message_id = await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'thread_name': self.room_group_name,
                'message_id': message_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        thread_name = event['thread_name']
        message_id = event['message_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'thread_name': thread_name,
            'id': message_id

        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        id = ChatModel(
            sender=username, message=message, thread_name=thread_name)
        id.save()
        return id.id


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_name = f'{group_id}'
        self.room_group_name = 'group_%s' % self.room_name
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        message_id = await self.save_message(username, self.room_group_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'thread_name': self.room_group_name,
                'message_id': message_id

            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        thread_name = event['thread_name']
        message_id = event['message_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'thread_name': thread_name,
            'id': message_id
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        id = GroupChat(
            sender=username, message=message, thread_name=thread_name)
        id.save()
        return id.id
