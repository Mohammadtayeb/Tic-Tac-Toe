from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

    def __str__(self) -> str:
        return f"{self.username} is id {self.pk}."
    
class RoomCode(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    room_code = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.room_code} is saved in database."
    
class JoinedRoom(models.Model):
    joiner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    joined = models.CharField(max_length=64)