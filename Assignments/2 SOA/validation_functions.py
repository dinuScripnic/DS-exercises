import jwt


SECRET_KEY = "burner123"


def generate_token(username):
    token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
    return token


def validate_token(token, valid_username: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = decoded_token["username"]
        if username == valid_username:
            return True
        else:
            return False
    except:
        return False

