from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    profile_pic=models.ImageField(upload_to='profiles',null=True,blank=True)
    address=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES=[
        ("draft","DRAFT"),
        ("published","PUBLISHED")
    ]
    title=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    body=models.CharField(max_length=200,blank=True,null=True)
    category=models.ManyToManyField(Category,blank=True)
    views=models.IntegerField(default=0)
    status=models.CharField(max_length=200,choices=STATUS_CHOICES,default="draft")

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} to the post {self.post.title}"
    
