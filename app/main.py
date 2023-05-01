import psycopg2
import time
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schema, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my app!"}

