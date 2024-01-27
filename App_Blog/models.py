from django.db import models
from django.contrib.auth.models import User
from App_Authentication.models import UserProfileModel

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_author')
    title = models.CharField(max_length=300, verbose_name='Title of your blog')
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField(verbose_name='Content of your blog')
    image = models.ImageField(upload_to='blog_images')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment_on_blog')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_on_blog_by_user')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "@" + str(self.user) + " commented on the blog - " + str(self.blog)

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='like_on_blog')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_on_blog_by_user')

    def __str__(self):
        return "@" + str(self.user) + " liked the blog - " + str(self.blog)