import requests 


# 1. Récupérer tous les utilisateurs (`/users`)
BASE_URL = "https://jsonplaceholder.typicode.com"
USERS_URL = f"{BASE_URL}/users"
POSTS_URL = f"{BASE_URL}/posts"

response = requests.get(USERS_URL)
users = response.json() 



# 2. Afficher le nom et l'email de chaque utilisateur
for user in users :
    print(f"user name = {user['name']} and user email = {user['email']}")


# 3. Récupérer tous les posts de l'utilisateur avec `userId=1`
response_userid1= requests.get(f"{POSTS_URL}?userId=1")
posts_userid1 = response_userid1.json() 

posts_user1 = response_userid1.json()
# print(f"Nombre de posts pour userId=1 : {posts_user1}")


# 4. Compter combien de posts chaque utilisateur a créé
response_post = requests.get(POSTS_URL)
posts = response_post.json()

user1 = 0
user2 = 0
user3 = 0
user4 = 0
user5 = 0
user6 = 0
user7 = 0
user8 = 0
user9 = 0
user10 = 0

for post in posts :
    if ['userId'] == 1 :
        user1 + 1
        print(f"Nombre de posts pour userId=1 : {user1}")
    if ['userId'] == 2 :
        user2 + 1
        print(f"Nombre de posts pour userId=1 : {user2}")
    if ['userId'] == 3 :
        user3 + 1
        print(f"Nombre de posts pour userId=1 : {user3}")
    if ['userId'] == 1 :
        user4 + 1
        print(f"Nombre de posts pour userId=1 : {user4}")


# 5. Récupérer les commentaires du post `id=1`
response_id1= requests.get(f"{POSTS_URL}?id=1")
posts_id1 = response_id1.json() 
print(posts_id1)