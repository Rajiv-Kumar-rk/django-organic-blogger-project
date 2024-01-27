from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics')
    discription = models.TextField(max_length=300)
    instagram_profile_link = models.URLField(blank=True, null=True)
    facebook_profile_link = models.URLField(blank=True, null=True)
    twitter_profile_link = models.URLField(blank=True, null=True)
    linkedin_profile_link = models.URLField(blank=True, null=True)
 
    def __str__(self):
        return str(self.user)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return "@" + str(self.follower) + " follow " + "@" + str(self.following)