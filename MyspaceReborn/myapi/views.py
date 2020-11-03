from .serializers import UserSerializer, PostSerializer
from .models import User, Post
from django.http import HttpResponse, JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from pyhunter import PyHunter
import clearbit

@csrf_exempt
def get_all_users(request):
    serializer = UserSerializer(User.objects.all().order_by('-num_posts_published'), many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def get_all_posts(request):
    serializer = PostSerializer(Post.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def signup_user(request):
    user_details = request.POST
    hunter = PyHunter('0c698973e3a9504076a297e93d34be9eb05aaa44')
    email = user_details['email']
    verification_result = hunter.email_verifier(email)
    is_email_verified = verification_result['score'] >= 65 #this is just a score for testing purposes, not my criteria for what's acceptable
    if not is_email_verified:
        return HttpResponse(content='Email could not be verified! Please enter a valid email address capable of receiving mail', status=403)
    company_location, company_name, facebook, location = get_enriched_details(email)
    new_user = User(name = user_details['name'], email = email, age = user_details['age'], birth_date = user_details['birth_date'],
                    location = location, facebook = facebook, company_name = company_name, company_location = company_location)
    new_user.save()
    return HttpResponse(
        content=f'User with id {new_user.id} signed up successfully',
        status=200
    )


def get_enriched_details(email):
    company_location, company_name, facebook, location = None, None, None, None
    clearbit.key = 'sk_eccb39c1cea7d84f1df1c743499c82b7'
    response = clearbit.Enrichment.find(email=email, stream=True)
    if response != None:
        if response['person'] is not None:
            if response['person']['location'] is not None:
                location = response['person']['location']
            if response['person']['facebook'] is not None:
                facebook = response['person']['facebook'][
                    'handle']  # assuming if 'facebook' key exists, 'handle' will as well
        if response['company'] is not None:
            if response['company']['name'] is not None:
                company_name = response['company']['name']
            if response['company']['location'] is not None:
                company_location = response['company']['location']
    return company_location, company_name, facebook, location


@csrf_exempt
def login_user(request):
    user_details = request.POST
    email = user_details['email']
    users = User.objects.filter(email = email)
    if len(users) == 0:
        return HttpResponse(
            content=f'User with email {email} not present in the system. Please register to publish posts',
            status=403)
    user = users[0]
    State.logged_in_user_id = user.id
    return HttpResponse(
        content=f'User with id {user.id} has logged in',
        status=200)

@csrf_exempt
def publish_post(request):
    post_details = request.POST
    post = Post(body = post_details['body'], user_id = State.logged_in_user_id, date = datetime.datetime.now())
    user = User.objects.filter(id = State.logged_in_user_id)[0]
    user.num_posts_published+= 1
    post.save()
    user.posts_published += f'{post.id}' if len(user.posts_published) == 0 else f',{post.id}'
    user.save()
    return HttpResponse(
            content=f'User with id {State.logged_in_user_id} published post successfully',
            status=200)


@csrf_exempt
def interact_post(request, post_id):
    interaction_type = "dislike" if "dislike" in request.path else "like"
    posts = Post.objects.filter(id = post_id)
    if len(posts) == 0:
        return HttpResponse(
            content=f'Post with id {post_id} does not exist',
            status=403)
    post = posts[0]
    if post.user_id == State.logged_in_user_id:
        return HttpResponse(
            content=f'You cannot {interaction_type} post with id {post_id} because it is your own post',
            status=403)
    user = User.objects.filter(id = State.logged_in_user_id)[0]
    if interaction_type == "like" and str(post_id) in user.liked_posts.split(','):
        return HttpResponse(
            content=f'Post with id {post_id} already liked by {State.logged_in_user_id}',
            status=403)
    user.likes_given = user.likes_given + (1 if interaction_type == "like" else -1)
    user.liked_posts += f'{post.id}' if len(user.liked_posts) == 0 else f',{post.id}'
    post.num_likes = post.num_likes + (1 if interaction_type == "like" else -1)
    post.save()
    user.save()
    return HttpResponse(
        content=f'User with id {State.logged_in_user_id} {interaction_type}d post with id {post_id} successfully',
        status=200
    )

class State:
    logged_in_user_id = -1