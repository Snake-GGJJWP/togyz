# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.color = self.scope['url_route']['kwargs']['color']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('msgType') == 'message':
            await self.send_message_to_group(
                text_data_json['message'],
                text_data_json['msgType']
            )
        if text_data_json.get('msgType') == 'move':
            print(f"{self.color} have made a move")
            await self.make_move(
                text_data_json['message'],
                text_data_json['msgType'],
                text_data_json['startField'],
                text_data_json['endField'],
            )

    async def send_message_to_group(self, message, msg_type):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_type': msg_type,
                'message': message,
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

    # Receive message from room group
    async def chat_message(self, event):
        msg_type = event['msg_type']
        message = event['message']
        color = event['color']

        # Send message to WebSocket
        if msg_type == 'message':
            await self.send(text_data=json.dumps({
                'msgType': msg_type,
                'message': message,
                'color': color
            }))
        elif msg_type == 'move':
            await self.send(text_data=json.dumps({
                'msgType': msg_type,
                'message': message,
                'startField': event['start_field'],
                'endField': event['end_field'],
                'color': color
            }))
