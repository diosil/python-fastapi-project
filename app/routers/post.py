from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils, oauth2
from ..database import engine, get_db
from sqlalchemy import func
from typing import Optional, List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#################### GET methods ####################

@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    ##### Version 1 - With calls to cursor ######
        #posts = cursor.execute("""SELECT * FROM posts """)
        #posts = cursor.fetchall()
        #print(posts)
        #return {"data": posts}
    ##### Version 2 - With calls to db session ######
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schema.PostOut)
def get_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ##### Version 1 - With calls to cursor ######
        #post = cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
        #post = cursor.fetchone()
        #if not post:
        #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                        detail=f'id {id} was not found')
        #return {"data": post}
    ##### Version 2 - With calls to db session ######
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} was not found')
    return post


#################### POST methods ####################

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #### Version 1 - With calls to cursor ######
        #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
        #new_post = cursor.fetchone()
        #conn.commit()
        #return {"data": new_post}
    ##### Version 2 - With calls to db session ######
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#################### DELETE methods ####################

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ##### Version 1 - With calls to cursor ######
    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", str(id))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    #if not deleted_post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                        detail=f'post with id {id} was not found')
    #
    #return Response(status_code=status.HTTP_204_NO_CONTENT)
    ##### Version 2 - With calls to db session ######
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform such action')

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#################### PUT methods ####################

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schema.Post)
def update_post(id: int, post_updated: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ##### Version 1 - With calls to cursor ######
    #cursor.execute("""UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *""", 
    #               (post_updated.title, post_updated.content, post_updated.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    #if not updated_post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                        detail=f'post with id {id} was not found')
    #return {"data": updated_post}
    ##### Version 2 - With calls to db session ######
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f'post with id {id} was not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform such action')
    post_query.update(post_updated.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()