import requests
from requests import get, post
import json
import names
import random
import datetime

p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]

def generate_post_body():
    return f'{random.choice(p_nouns)} {random.choice(p_verbs)} {random.choice(p_nouns).lower()} {random.choice(infinitives)}'

with open('C:/Users/felix/Desktop/bot_rules.json') as file:
    data = json.load(file)
    number_of_users = data['number_of_users']
    max_posts_per_user = data['max_posts_per_user']
    max_likes_per_user = data['max_likes_per_user']

start_date = datetime.date(1900, 1, 1)
user_login_credentials = []

def sign_up_users():
    global i, email, pload, response
    for i in range(number_of_users):
        birth_date = start_date + datetime.timedelta(days=random.randint(1, 120 * 365))
        age = datetime.datetime.now().year - birth_date.year
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = f'{first_name}.{last_name}@gmail.com'
        user_login_credentials.append(email)
        pload = {'name': f'{first_name} {last_name}', 'email': email, 'age': age, 'birth_date': str(birth_date)}
        response = post('http://localhost:8000/signup', data=pload)
        print(response.text)

def publish_posts():
    global email, pload, response, i
    for email in user_login_credentials:
        pload = {'email': email}
        response = post('http://localhost:8000/login', data=pload)
        print(response.text)
        for i in range(random.randint(0, max_posts_per_user)):
            pload = {'body': generate_post_body()}
            response = post('http://localhost:8000/user/publish', data=pload)
            print(response.text)

def like_posts():
    global post, pload, response, likes_given
    posts = get('http://localhost:8000/get_posts').json()
    users = get('http://localhost:8000/get_users').json()
    # users are already sorted by most posts
    eligible_users_to_zero_like_posts = {}
    for post in posts:
        if post['num_likes'] == 0:
            if post['user_id'] not in eligible_users_to_zero_like_posts:
                eligible_users_to_zero_like_posts[post['user_id']] = []
            eligible_users_to_zero_like_posts[post['user_id']].append(post['id'])
    eligible_users = [*eligible_users_to_zero_like_posts]
    for user in users:
        pload = {'email': user['email']}
        response = requests.post('http://localhost:8000/login', data=pload)
        likes_given = 0
        while likes_given < max_likes_per_user:
            # IF NO MORE ELIGIBLE USERS TO LIKE, OR I AM THE ONLY ONE LEFT
            if len(eligible_users) == 0 or len(eligible_users) == 1 and eligible_users[0] == user['id']:
                break
            selected_user = random.choice(eligible_users)
            while selected_user == user['id']:
                selected_user = random.choice(eligible_users)
            posts_to_like = [user['posts_published'] for user in users if user['id'] == selected_user][0].split(',')
            selected_post = int(random.choice(posts_to_like))
            if selected_post in eligible_users_to_zero_like_posts[selected_user]:
                eligible_users_to_zero_like_posts[selected_user].remove(
                    selected_post)  # the post has no longer zero likes
                if len(eligible_users_to_zero_like_posts[selected_user]) == 0:
                    del eligible_users_to_zero_like_posts[selected_user]
                    eligible_users.remove(selected_user)
            response = requests.post(f'http://localhost:8000/user/like/{selected_post}')
            print(response.text)
            likes_given += 1

sign_up_users()
publish_posts()
like_posts()