from app.database.movies import Movies
from app.external import social_media

from fastapi import FastAPI

app = FastAPI()


@app.get("/get_all")
def get_all():
    return Movies.get_all()


@app.get("/posts")
def get_posts():
    return social_media.get_posts()


@app.get("/photos")
def get_photos():
    return social_media.get_photos()


@app.get("/comments")
def get_comments():
    return social_media.get_comments()
