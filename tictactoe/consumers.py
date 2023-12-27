import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


users_list = []
class PlayConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = "playing_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        user_name = self.scope['user'].username
        if user_name not in users_list:
            users_list.append(user_name)

        # Check that the users list must not be more than two
        if len(users_list) <= 2:
            print("This is list: ")
            print(users_list)
            self.accept()

    def disconnect(self, close_code):
        # Leaving the room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive game move from websocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        row = text_data_json["row"]
        column = text_data_json["column"]
        id = text_data_json["id"]



        # Sending players move to the room as a text 
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "game_move",
                "row": row,
                "column": column,
                "id": id
            }
        )

    def game_move(self, event):
        row = event["row"]
        column = event["column"]
        id = event["id"]

        self.send(text_data=json.dumps({
            "row": row,
            "column": column,
            "id": id
        }))
