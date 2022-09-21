from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    post_text         = models.CharField(max_length=140)
    post_by    = models.ForeignKey(User, on_delete=models.PROTECT)
    post_time = models.DateTimeField()


class Profile(models.Model):
    bio = models.CharField(max_length=200)
    user= models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type=models.CharField(max_length=50)
    following= models.ManyToManyField(User, related_name="followers")

class Comment(models.Model):
    comment_text         = models.CharField(max_length=140)
    comment_by    = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_time = models.DateTimeField(auto_now=True)
    comment_is_under_post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)


