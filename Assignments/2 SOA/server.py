# Server that handles requests from the client and sends back the response, but first uses authentication to verify the client using JWT


from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from validation_functions import generate_token, validate_token

from typing import Optional


""" john = User(username="john", password="password")
john.role = Role.Administrator



print(john.role)
"""
from enum import Enum

users = {}


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


app = FastAPI()


# authentication of the user with JWT

users = []
usernames = []
tokens = {}


# create a user with a role and a token
@app.post("/auth/user/")
async def create_user(username, password, new_role, token):
    tokens[username] = token
    if validate_token(token, username):
        print(usernames)
        if username not in usernames:
            
            print("Token is valid \n")
            user = User(username=username, password=password)
            user.role = new_role
            users.append(user)
            usernames.append(username)
            return 200
           
        else:
            return "User already exists" , 409
    else:
        return "Token is invalid", 498


# get the user role by username
@app.get("/auth/get_users/")
async def get_user(domestic_username,token,target_username):
    if validate_token(token,domestic_username):
        if target_username in usernames:
            for person in users:
                if person.username == target_username:
                    return [target_username,person.role], 200
        else:
            return "User does not exist", 404
    else:
        #invalid token = 498
        return "Invalid token", 498
    
        
# delete a user by username
@app.delete("/auth/delete_user/")
async def delete_user(username, token):
    if validate_token(token,username):
        # check if user exists
        if username in usernames:
            # delete user
            for user in users:
                if user.username == username:
                    users.remove(user)
                    usernames.remove(username)
                    return [username , "User deleted"], 200
        else:
            return "User does not exist", 404
    else:
        return "Invalid token", 498


# get all users
@app.get("/auth/get_all_users/")
async def get_all_users(token,username):
    output = []
    print(usernames)
    if validate_token(token,username):
        print("Token is valid \n")
        print("users", users)
        for person in users:
            output.append(person.username)
        return output, 200
    else:
        #invalid token = 498
        return "Invalid token", 498
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)

    
