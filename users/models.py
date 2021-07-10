from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/profile_default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'  

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" height="50">') 

    image_tag.short_description = 'Profile Pic'
