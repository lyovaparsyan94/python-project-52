from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    def __str__(self):
        return self.get_full_name()

