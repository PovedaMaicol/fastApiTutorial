from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

movies = [
    {
        "id": 1, 
        "title": "The Shawshank Redemption", 
        "overview": "Two imprisoned men",
        "year": 1994,
        "rating": 9.3,
        "category": "Drama"
    }
]

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


@app.get("/", tags=["Home"])
def home():
    return "Hola mundo!"

@app.get("/movies", tags=["Home"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["Home"])
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return []