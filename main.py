from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Optional field, if user doesn't provide value then it will default to True
    rating: Optional[int] = None  # Complete optional, if user doesn't provide value then nothing will be assigned


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_post():
    return {"data": "This is your post"}


@app.post("/create_posts")
def create_post(new_post: Post):
    print(new_post)
    print(new_post.dict())
    return {"data": new_post}
# title str, content str
