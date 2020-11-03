from django.urls import include, path
from rest_framework import routers
from . import views
from . models import User
from . models import Post

router = routers.DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('signup', views.signup_user),
    path('login', views.login_user),
    path('user/publish', views.publish_post),
    path('user/like/<int:post_id>', views.interact_post),
    path('user/dislike/<int:post_id>', views.interact_post),
    path('get_posts', views.get_all_posts),
    path('get_users', views.get_all_users)
]

User.objects.all().delete()
Post.objects.all().delete()