import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import User
from message.models import MessageRoom, RoomMessage
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        route = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_name = str(object=route).split(sep='&')[0]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = str(object=route).split(sep='&')[1]
        self.room_obj = await MessageRoom.objects.aget(pk = self.room_name)
        self.user_obj = await User.objects.aget(pk = self.user)
        self.user_in_room = await self.room_obj.users.all().acontains(obj=self.user_obj)
        if self.user_in_room:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            self.close(code=4903)


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(s=text_data)
        message = text_data_json["message"]
        user = text_data_json["user"]
        user_obj = await User.objects.aget(pk = user)
        message_obj = await RoomMessage.objects.acreate(room = self.room_obj, messenger = user_obj, body = message)
        await sync_to_async(func=lambda: self.room_obj.save())()
        date = str(object=f'{message_obj.created_at.date()} {message_obj.created_at.time()}')
        picture = '/static/assets/img/account.jpg'
        if user_obj.profile_picture:
            picture = str(object=user_obj.profile_picture.url)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                'user': user,
                'send_at':date,
                'user_profile_picture':str(object=picture)
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        send_at = event["send_at"]
        profile = event["user_profile_picture"]
        await self.send(text_data=json.dumps(obj={"message": message, "profile": profile, "user": user, "send_at": send_at}))