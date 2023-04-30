from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected successfully!')
        break
    except Exception as Error:
        print('Connection to database failed')
        print('Error: ', Error)
        time.sleep(2)

my_posts = [{"title":"title post 1", "content" : "content of post 1", "id": 1}, {"title":"favourite foods", "content" : "i like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
                
@app.get("/")
def root():
    return {"message": "Welcome to my app!"}

@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.get("/posts/{id}")
def get_single_post(id: int):
    post = cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} was not found')
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", str(id))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post_updated: Post):

    cursor.execute("""UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *""", 
                   (post_updated.title, post_updated.content, post_updated.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')

    return {"data": updated_post}

