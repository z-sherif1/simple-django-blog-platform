from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #kol user leh profile wa7ed bas
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/',null=True, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=150)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL, related_name='posts',  null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username} - {self.post.title}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name