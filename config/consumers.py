from channels.generic.websocket import WebsocketConsumer
import json
from hr.models import JobPost

class DateTimeUpdate(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['job_id']
        self.room_group_name = 'job_%s' % self.room_name
        print('connect')
        return super().connect()
    # Receive message from WebSocket---------------------------------------------
    # def receive(self, text_data=None, bytes_data=None):
    #     """ Called when a connection is established"""
    #     self.accept()  # Accept the connection - this sends a reply back to the client

    def disconnect(self, code):
        return super().disconnect(code)