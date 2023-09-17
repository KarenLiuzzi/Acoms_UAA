import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))
        
    def enviar_notificacion_a_usuario(self, user_id, message):
        channel_layer = get_channel_layer()
        channel_name = f"user_{user_id}"
        # Usa async_to_sync para añadir la conexión actual al grupo de canales
        async_to_sync(channel_layer.group_add)(channel_name, self.channel_name)
        async_to_sync(channel_layer.group_send)(channel_name, {
            "type": "send_notification",
            "message": message,
        })