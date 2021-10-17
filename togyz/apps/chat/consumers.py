# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Game


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.color = self.scope['url_route']['kwargs']['color']  # Our color
        self.username = self.scope['url_route']['kwargs']['username']  # Associating a channel with a user
        self.room_group_name = 'chat_%s' % self.room_name
        self.started = False

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        '''if self.color != 'spec':
            await self.opponent_joined()'''

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # Chat message
        if text_data_json.get('msgType') == 'message':
            await self.send_message_to_group(
                text_data_json['message'],
                text_data_json['msgType']
            )
        # Move message
        if text_data_json.get('msgType') == 'move':
            print(f"{self.color} have made a move")
            await self.make_move(
                text_data_json['message'],
                text_data_json['msgType'],
                text_data_json['startField'],
                text_data_json['endField'],
            )

    # |SEND MESSAGES TO THE GROUP|
    # --------------------------------------------
    async def send_message_to_group(self, message, msg_type):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_type': msg_type,
                'message': message,
                'message_from': self.username,
                'color': self.color
            }
        )

    async def make_move(self, message, msg_type, start, end):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_type': msg_type,
                'message': message,
                'start_field': start,
                'end_field': end,
                'color': self.color
            }
        )

    '''async def opponent_joined(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_type': 'opponent_joined',
                'color': self.color
            }
        )

    async def opponent_joined_echo(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_type': 'opponent_joined_echo',
                'color': self.color
            }
        )'''
    # --------------------------------------------

    # Receive message from room group
    async def chat_message(self, event):
        msg_type = event['msg_type']

        # Send message to WebSocket
        # Chat message
        if msg_type == 'message':
            await self.send(text_data=json.dumps({
                'msgType': msg_type,
                'message': event['message'],
                'messageFrom': event['message_from'],
                'color': event['color']
            }))
        # Move message
        elif msg_type == 'move':
            await self.send(text_data=json.dumps({
                'msgType': msg_type,
                'message': event['message'],
                'startField': event['start_field'],
                'endField': event['end_field'],
                'color': event['color']
            }))
        '''# When player's opponent joined (it can't be seen by anyone except this player)
        elif (msg_type == 'opponent_joined') and (self.color != event['color']) and (event['color'] != 'spec') and (self.color != 'spec'):
            await self.opponent_joined_echo()
            if not self.started:
                await self.send(text_data=json.dumps({
                    'msgType': 'opponent_joined'
                }))
                self.started = True
        # Echoing back to the opponent (it can't be seen by anyone except the opponent)
        elif ((msg_type == 'opponent_joined_echo') and (self.color != event['color']) and (event['color'] != 'spec') and (self.color != 'spec')):
            if not self.started:
                await self.send(text_data=json.dumps({
                    'msgType': 'opponent_joined'
                }))
                self.started = True'''


# GAME HANDLER
class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game = Game.objects.filter(name=self.scope['url_route']['kwargs']['room_name'])[0]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.color = self.scope['url_route']['kwargs']['color']
        self.history = self.game.history
        self.current_position = self.game.current_position
        self.move_number = 0
        self.started = False

        self.room_group_name = 'game_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        if self.color != 'spec':
            self.opponent_joined()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        if not self.started:
            self.send(json.dumps({
                'msgType': 'denied',
                'comment': 'Game has not been started yet'
            }))
            return
        else:
            self.send(json.dumps({
                'msgType': 'denied',
                'comment': 'There is nothing here now... But game is on'
            }))
            return

        text_data_json = json.loads(text_data)
        self.current_position[text_data_json['startField']] = ''

        self.history[self.move_number] = ''

    def opponent_joined(self):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_type': 'opponent_joined',
                'color': self.color
            }
        )

    def opponent_joined_echo(self):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_type': 'opponent_joined_echo',
                'color': self.color
            }
        )

    def chat_message(self, event):
        msg_type = event['msg_type']

        # When player's opponent joined (it can't be seen by anyone except this player)
        if (msg_type == 'opponent_joined') and (self.color != event['color']) and (event['color'] != 'spec') and (self.color != 'spec'):
            self.opponent_joined_echo()
            if not self.started:
                self.send(json.dumps({
                    'msgType': 'opponent_joined'
                }))
                self.started = True

        # Echoing back to the opponent (it can't be seen by anyone except the opponent)
        if (msg_type == 'opponent_joined_echo') and (self.color != event['color']) and (event['color'] != 'spec') and (self.color != 'spec'):
            if not self.started:
                self.send(json.dumps({
                    'msgType': 'opponent_joined'
                }))
                self.started = True
