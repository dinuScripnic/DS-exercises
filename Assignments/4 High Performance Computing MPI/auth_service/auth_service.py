from fastapi import FastAPI, HTTPException
from other.schemas import ChangeRole, Login, Role, User
from other.logging_functionality import create_log_file, write_log
from auth import AuthHandler
from users import db, get_role, get_user
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
authHandler = AuthHandler()
# allow all origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# this is a test
@app.get("/auth/users/")
async def get_users():
    return db


@app.get("/auth/role/")
async def return_role(token: str) -> tuple:
    user = authHandler.decode_token(
        token
    )  # decode the token and get the dict with data
    role = get_role(user)  # get the role from the database
    return user, role  # return the role


@app.post("/auth/login/")
async def login(auth_details: Login) -> dict:
    """
    login function, returns a token if the user exists and the password is correct
    the token is used to access the other endpoints

    Args:
        auth_details (Login): authentication details(username and password)

    Raises:
        HTTPException: if the user doesn't exist
        HTTPException: if the password is incorrect

    Returns:
        dict: token
    """
    user = get_user(auth_details.username)  # get the user from the database
    if user is None:  # if the user doesn't exist, raise an error
        raise HTTPException(status_code=401, detail="Invalid username")
    if not authHandler.verify_password(
        auth_details.password, user.password
    ):  # if the password is incorrect, raise an error
        raise HTTPException(status_code=401, detail="Invalid password")
    token = authHandler.encode_token(
        user.username
    )  # if the user exists and the password is correct, generate a token
    return {"token": token}  # return the token


@app.post("/auth/manage/")
async def create_user(token: str, user: User) -> int:
    """
    Creates a new user and returns the success code.

    Args:
        token (str): authentication token
        user (User): user data to be added

    Raises:
        HTTPException: username taken
        HTTPException: user doesn't have admin role

    Returns:
        int: success code
    """
    admin = authHandler.decode_token(
        token
    )  # decode the token and get the dict with data
    admin = get_user(admin)  # get the user from the database
    if admin.role == Role.Administrator:  # check the role
        if any(
            x.username == user.username for x in db
        ):  # check the existance of the username in the database
            raise HTTPException(
                status_code=409, detail="Username taken"
            )  # if the username exists, raise an error
        db.append(
            User(
                username=user.username,
                password=authHandler.get_password_hash(user.password),
                role=user.role,
            )
        )  # if the username doesn't exist, add the user to the database
        write_log("User added", 200)
        return 200  # return 200 if the user was added
    else:
        raise HTTPException(status_code=403, detail="Not admin")


@app.put("/auth/manage/")
async def change_role(token: str, user: ChangeRole) -> int:
    """
    Changes the role of a user and returns the success code.

    Args:
        token (str): authentication token
        user (ChangeRole): user data to be changed( username and role)

    Raises:
        HTTPException: user not found
        HTTPException: request user doesn't have admin role

    Returns:
        int: success code
    """
    request = authHandler.decode_token(token)
    admin = get_user(request)
    if admin.role == Role.Administrator:
        change = get_user(user.username)
        if change is None:
            raise HTTPException(status_code=404, detail="User not found")
        change.role = user.role
        write_log("Role changed", 200)
        return 200
    else:
        raise HTTPException(status_code=403, detail="Not admin")


@app.delete("/auth/manage/")
async def delete_user(token: str, username: str) -> int:
    """
    Deletes a user and returns the success code.

    Args:
        token (str): authentication token
        username (str): username of the user to be deleted

    Raises:
        HTTPException: user not found
        HTTPException: doesn't have admin role

    Returns:
        int: success code
    """
    admin = authHandler.decode_token(token)
    admin = get_user(admin)
    if admin.role == Role.Administrator:
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.remove(user)
        write_log("User deleted", 200)
        return 200
    else:
        raise HTTPException(status_code=403, detail="Not admin")


if __name__ == "__main__":
    import uvicorn
    create_log_file()

    # run on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
