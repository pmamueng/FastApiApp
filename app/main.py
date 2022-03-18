from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import engine, get_db
from app.config import Settings
from app.routers import auth, post, user, vote


#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://www.google.com"
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API, successfully deployed from CI/CD pipeline"}


# app_posts = [{"title": "example_title_1", "content": "example_content_1", "id": 1},
#              {"title": "example_title_2", "content": "example_content_2", "id": 2}]


# def find_post(id):
#     for p in app_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(app_posts):
#         if p["id"] == id:
#             return i


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
