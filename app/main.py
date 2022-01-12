import psycopg2
import time

from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Optional field, if user doesn't provide value then it will default to True
    # rating: Optional[int] = None  # Complete optional, if user doesn't provide value then nothing will be assigned


while True:
    try:
        db_connection = psycopg2.connect(host='localhost', database='FastApiApp', user='postgres', password='postgres',
                                        cursor_factory=RealDictCursor)
        cursor = db_connection.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print(f"Connection to database failed.")
        print("Error: ", error)
        time.sleep(2)


app_posts = [{"title": "example_title_1", "content": "example_content_1", "id": 1},
             {"title": "example_title_2", "content": "example_content_2", "id": 2}]


def find_post(id):
    for p in app_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(app_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


###### Tranditional Database Integration ######
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data": posts}


# @app.get("/posts/{id}")
# def get_post(id: int):  # turn id into string and FastAPI will validate it
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", [id])
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
#     return {"data": post}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     db_connection.commit()
#     return {"data": new_post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [id])
#     deleted_post = cursor.fetchone()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
#     db_connection.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
#     updated_post = cursor.fetchone()
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
#     db_connection.commit()
#     return {"message": f"post with id: {id} was successfully updated", "data": updated_post}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return {"message": f"post with id: {id} was successfully updated", "data": post_query.first()}
