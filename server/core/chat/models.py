from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chatrooms_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chatrooms_user2', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.room_name:
            self.room_name = f'room_{min(self.user1.id, self.user2.id)}_{max(self.user1.id, self.user2.id)}'
        super().save(*args, **kwargs)