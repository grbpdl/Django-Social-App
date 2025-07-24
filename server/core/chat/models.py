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

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE,blank=True, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"