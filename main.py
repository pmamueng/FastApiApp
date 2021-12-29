from fastapi import FastAPI
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


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": app_posts}


@app.get("/posts/{id}")
def get_post(id: int):  # turn id into string and FastAPI will validate it
    post = find_post(id)  # id is a string from path parameter, have to convert it to integer
    return {"data": post}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    app_posts.append(post_dict)
    return {"data": post_dict}

