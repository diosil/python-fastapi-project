from passlib.context import CryptContext

def hash(password: str):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i