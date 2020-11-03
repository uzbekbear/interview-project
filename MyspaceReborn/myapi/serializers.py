from rest_framework import serializers
from .models import User
from .models import Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'age', 'birth_date', 'posts_published', 'num_posts_published', 'likes_given', 'email')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'body', 'user_id', 'date', 'num_likes')