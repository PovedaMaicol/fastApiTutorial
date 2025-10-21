from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel 
from typing import Optional, List

app = FastAPI()


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str
    
class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str

movies = [
    {
        "id": 1, 
        "title": "The Shawshank Redemption", 
        "overview": "Two imprisoned men",
        "year": 1994,
        "rating": 9.3,
        "category": "Drama"
    },
      {
        "id": 2, 
        "title": "Optra automatico", 
        "overview": "A car that drives itself",
        "year": 1992,
        "rating": 9.3,
        "category": "Acción"
    }
]

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


@app.get("/", tags=["Home"])
def home():
    return "Hola mundo!"

@app.get("/movies", tags=["Movies"])
def get_movies() -> List[Movie]:
    return movies


@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return movie
    return []

@app.get('/movies/', tags=["Movies"])
def get_movie_by_category(category: str, year: int) -> Movie:
    for movie in movies:
        if movie['category'] == category:
            return movie
    return []

@app.post("/movies", tags=["Movies"])
def create_movie(movie: Movie):
    movies.append(movie.model_dump())
    return movies

@app.put('/movies/{id}', tags=["Movies"])
def update_movie(
    id: int, movie: MovieUpdate
    ) -> List[Movie]:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return movies
    return []
    
    
@app.delete('/movies/{id}', tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return movies