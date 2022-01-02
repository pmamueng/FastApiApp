from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Optional field, if user doesn't provide value then it will default to True
    rating: Optional[int] = None  # Complete optional, if user doesn't provide value then nothing will be assigned


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


@app.get("/posts")
def get_posts():
    return {"data": app_posts}


@app.get("/posts/{id}")
def get_post(id: int):  # turn id into string and FastAPI will validate it
    post = find_post(id)  # id is a string from path parameter, have to convert it to integer
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    app_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    app_posts.pop(index)
    return {"message": f"post with id: {id} was successfully deleted"}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id  # Set new post_dict to have the same id
    app_posts[index] = post_dict  # Update (set) the old post in index with the new post_dict
    return {"message": f"post with id: {id} was successfully updated"}
