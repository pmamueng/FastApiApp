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


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_post():
    return {"data": app_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    app_posts.append(post_dict)
    return {"data": post_dict}
