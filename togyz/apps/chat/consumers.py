# chat/consumers.py
import json
from itertools import cycle
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Game


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.user = self.scope['user']
        print(self.user)
        if self.user:
            self.username = self.user.username
        else:
            self.username = 'Anonym'

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
        # Chat message
        if text_data_json.get('msgType') == 'message':
            await self.send_message_to_group(
                text_data_json['message'],
                text_data_json['msgType']
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
            }
        )

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
            }))


# GAME HANDLER
class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']

        self.room_group_name = 'game_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        game = Game.objects.filter(name=self.room_name)[0]

        if self.user.username == game.player_white:
            self.color = 'white'
        elif self.user.username == game.player_black:
            self.color = 'black'
        else:
            self.color = 'spec'

        self.started = game.is_started
        self.red_sphere = False
        current_position = json.loads(game.current_position)
        if self.color == 'white' and sum([1 for i in range(1, 10) if current_position[str(i)] == 'X']):
            self.red_sphere = True
        elif self.color == 'black' and sum([1 for i in range(10, 19) if current_position[str(i)] == 'X']):
            self.red_sphere = True

        self.accept()

        self.send_back(msg_type='move', current_position=current_position, winner=game.winner)

        if self.color != 'spec':
            self.send_to_group(msg_type='opponent_joined', color=self.color)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data = json.loads(text_data)
        if not self.started:
            self.send_back(msg_type='denied', comment='Game has not been started yet')
            return

        if text_data['msg_type'] == 'move':
            self.make_move(text_data['startField'])

    def make_move(self, start_field):
        def update(current_position, history, color_turn, winner):
            print(f"{winner} WON")
            self.send_to_group(msg_type='move', current_position=current_position, winner=winner)
            game.current_position = json.dumps(current_position)
            game.history = json.dumps(history)
            game.color_turn = color_turn
            if winner:
                game.winner = winner
                game.is_finished = True
            game.save()

        def define_winner(current_position, white, black):
            if current_position['white_pool'] > current_position['black_pool']:
                return white
            elif current_position['white_pool'] < current_position['black_pool']:
                return black
            else:
                return "draw"

        def get_winner(game, board_ind, current_position):
            winner = None

            # Total amount of kums in white and black fields.
            # Basically counts all values in current_position indexes of which
            # corresponds to given color.
            # NOTE: there may be string value such as 'X' in current_position
            # so we must ensure we don't count them
            white_total = sum([current_position[str(i)] for i in board_ind['white'] if current_position[str(i)] != 'X'])
            black_total = sum([current_position[str(i)] for i in board_ind['black'] if current_position[str(i)] != 'X'])

            end_point_position = {str(i): 0 for i in range(1, 18)} | {'white_pool': current_position['white_pool'], 'black_pool': current_position['black_pool']}
            if self.color == 'white' and black_total == 0:
                current_position['white_pool'] += white_total
                winner = define_winner(current_position, white=game.player_white, black=game.player_black)
                current_position = end_point_position
            elif self.color == 'black' and white_total == 0:
                current_position['black_pool'] += black_total
                winner = define_winner(current_position, white=game.player_white, black=game.player_black)
                current_position = end_point_position
            return winner, current_position

        game = Game.objects.filter(name=self.room_name)[0]
        history = json.loads(game.history)
        current_position = json.loads(game.current_position)
        color_turn = game.color_turn

        if game.is_finished:
            self.send_back(msg_type='denied', comment='Game has been finished already')

        board_ind = {'white': list(map(str, range(1, 10))), 'black': list(map(str, range(10, 19)))}

        # if signal was sent from a spectator
        # or field index doesn't match allowed field indexes for this color
        if not board_ind.get(self.color) or start_field not in board_ind.get(self.color):
            self.send_back(msg_type='denied', comment='Illegal move')
            return

        # if someone made 2 moves in a row
        if (self.color != color_turn):
            self.send_back(msg_type='denied', comment='Not your turn yet')
            return

        kum = current_position.get(start_field)

        if kum is None:
            self.send_back(msg_type='denied', comment='Couldn\'t find a field with such index')
            return
        elif kum == 0 or kum == 'X':
            self.send_back(msg_type='denied', comment='Illegal move')
            return

        if self.color == 'white':
            color_turn = 'black'
        elif self.color == 'black':
            color_turn = 'white'

        if kum == 1:
            current_position[start_field] = 0
            if start_field == '18' or (current_position[str(int(start_field) + 1)] == 'X' and self.color == 'white'):
                current_position['black_pool'] += 1
            elif start_field == '9' or (current_position[str(int(start_field) + 1)] == 'X' and self.color == 'black'):
                current_position['white_pool'] += 1
            else:
                current_position[str(int(start_field) + 1)] += 1
            winner, current_position = get_winner(game, board_ind, current_position)
            update(current_position, history, color_turn, winner)
            return

        current_position[start_field] = 0

        j = 0
        indexes = cycle(list(range(int(start_field), 19)) + list(range(1, int(start_field))))
        while j < kum:
            i = indexes.__next__()
            if current_position[str(i)] == "X":
                if str(i) in board_ind['white']:
                    current_position['black_pool'] += 1
                else:
                    current_position['white_pool'] += 1
                j += 1
                continue
            current_position[str(i)] += 1
            j += 1
            if self.color == 'white' and i == 9 and j < kum:
                current_position['white_pool'] += 1
                j += 1
            if self.color == 'black' and i == 18 and j < kum:
                current_position['black_pool'] += 1
                j += 1
        print(i)
        print(board_ind.get(self.color))
        if str(i) not in board_ind.get(self.color) and current_position[str(i)] != 'X':
            if current_position[str(i)] % 2 == 0:
                current_position[f'{self.color}_pool'] += current_position[str(i)]
                current_position[str(i)] = 0
            elif current_position[str(i)] == 3 and i not in {1, 10} and current_position[str((i - 9) % 18)] != "X" and not self.red_sphere:
                current_position[f'{self.color}_pool'] += current_position[str(i)]
                current_position[str(i)] = 'X'
                self.red_sphere = True

        history.append(f'{start_field} - {i}')

        winner, current_position = get_winner(game, board_ind, current_position)

        update(current_position, history, color_turn, winner)

    def chat_message(self, event):
        msg_type = event['msg_type']

        if (msg_type == 'move'):
            self.send_back(msg_type=msg_type, current_position=event['current_position'], winner=event['winner'])

        # When player's opponent joined (it can't be seen by anyone except this player)
        if (msg_type == 'opponent_joined') and (self.color != event['color']) and (event['color'] != 'spec') and (self.color != 'spec'):
            self.send_to_group(msg_type='opponent_joined_echo', color=self.color)
            if not self.started:
                self.send_back(msg_type='opponent_joined')
                self.started = True

        # Echoing back to the opponent (it can't be seen by anyone except the opponent)
        if (msg_type == 'opponent_joined_echo') and (self.color != event['color']) and (event['color'] != 'spec') and (self.color != 'spec'):
            if not self.started:
                self.send_back(msg_type='opponent_joined')
                self.started = True

    def send_back(self, msg_type=None, **kwargs):
        text_data = {'msgType': msg_type} | kwargs  # merging two dicts
        self.send(json.dumps(text_data))

    @async_to_sync
    async def send_to_group(self, msg_type=None, **kwargs):
        text_data = {'type': 'chat_message', 'msg_type': msg_type} | kwargs
        await self.channel_layer.group_send(self.room_group_name, text_data)
