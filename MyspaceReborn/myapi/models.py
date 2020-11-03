from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    age = models.IntegerField()
    birth_date = models.DateField()
    location = models.CharField(max_length=60, null=True, default=None)
    facebook = models.CharField(max_length=60, null=True, default=None)
    company_name = models.CharField(max_length=60, null=True, default=None)
    company_location = models.CharField(max_length=60, null=True, default=None)
    likes_given = models.IntegerField(default = 0)
    num_posts_published = models.IntegerField(default = 0)
    liked_posts = models.CharField(max_length = 600, blank=True, null=True,default='')
    posts_published = models.CharField(max_length=600, blank=True, null=True, default='')


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=100)
    user_id = models.IntegerField()
    date = models.DateTimeField()
    num_likes = models.IntegerField(default = 0)
