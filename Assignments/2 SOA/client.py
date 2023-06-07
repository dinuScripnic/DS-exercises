import requests


from enum import Enum

from validation_functions import generate_token, validate_token


class Role(Enum):
    Administrator = 1

    Secretary = 2

    Manager = 3

    def __str__(self):
        return f"{self.value}"


class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.role = None
        self.token = None
    
    def __str__(self):
        return f"{self.username} {self.password} {self.role}"


def initialize_user(user_name, password, role):
    user = User(username=user_name, password=password)
    if role == "admin":
        user.role = Role.Administrator
    if role == "secretary":
        user.role = Role.Secretary
    if role == "manager":
        user.role = Role.Manager
    if role != "admin" and role != "secretary" and role != "manager":
        print("Invalid role")
        return None
    
    token = generate_token(user_name)
    user.token = token

    return user,token
def post_user(who,user):
    if who.role == Role.Administrator:
            
        url = "http://localhost:8000/auth/user/"
        params = {
            "user_role": user.role,
            "username": user.username,
            "password": user.password,
            "new_role": user.role,
            "token": user.token,
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            print("Creating user on server")
            data = response.json()
            print(data)
    else:
        print("You are not an admin")
    



# get a user from the server with a username = Secretaries only
def get_user_role(user, target_username):
    if user.role == Role.Secretary:
            
        url = "http://localhost:8000/auth/get_users"
        params = {
            "domestic_username": user.username,
            "token": user.token,
            "target_username": target_username,        
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Getting users from server")
            data = response.json()
            print(data)
    else:
        print("You are not an admin")
    return None

def get_all_users(user):
    url = "http://localhost:8000/auth/get_all_users/"
    response = requests.get(url,params={"token":user.token,"username":user.username})
    if response.status_code == 200:
        print("Getting users from server")
        data = response.json()
        print(data)


def delete_user(who,to_be_deleted):
    if who.role == Role.Administrator:
        url = "http://localhost:8000/auth/delete_user/"
        params = {
            "username": to_be_deleted.username,
            "token": bob_the_spy.token,
        }
    else:
        print("You are not an admin")
        return None

    response = requests.delete(url, params=params)
    if response.status_code == 200:
        print("Deleting user from server")
        data = response.json()
        print(data)

if __name__ == "__main__":
    #=================ADMIN CREATION=================
    john,token1 = initialize_user("john", "password", "admin")
    post_user(john,john)
    # response: 200

    #=================SECRETARY CREATION=================
    matt,token2 = initialize_user("matt","password123","secretary")
    post_user(john,matt)
    # response: 200

    #=================SECRETARY SPY=================
    bob_the_spy,token3 = initialize_user("bob","Iam spying","secretary")
    post_user(john,bob_the_spy)
    # response: 200

    #=================MANAGER CREATION=================
    martin,token4 = initialize_user("martin","password321","manager")
    post_user(john,martin)
    # response: 200

    #=================GET ALL USERS=================
    get_all_users(john)
    # response: [['john', 'matt', 'martin','bob'], 200]

    #=================GET USER ROLE=================
    #secretary task
    get_user_role(bob_the_spy,"martin")
    # response: [['martin','3'], 200]

    #=================DELETE USER=================
    delete_user(john,bob_the_spy)

    #=================GET ALL USERS=================
    get_all_users(john)
    # response: [['john', 'matt', 'martin',], 200]