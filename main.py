import datetime
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field 
from typing import Optional, List

# pydantic es para manejo de errores
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
    
class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=15, default="movie")
    overview: str = Field(min_length=15, max_length=50, default="Este es un overview")
    year: int = Field(le=datetime.date.today().year, ge=1900, default=2023)
    rating: float = Field(ge=0, le=10, default=10)
    category: str = Field(min_length=5, max_length=20, default="category")
    
    model_config = {
        'json_schema_extra':{
            'example': {
                'id': 3,
                'title': 'Movie Example',
                'overview': 'This is an example overview for a movie.',
                'year': 2023,
                'rating': 8.5,
                'category': 'Drama'
            }
        }
    }

movies: List[Movie] = []

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


@app.get("/", tags=["Home"])
def home():
    return "Hola mundo!"

@app.get("/movies", tags=["Movies"])
def get_movies() -> List[Movie]:
    return [movie.model_dump() for movie in movies]



@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return movie.model_dump()
    return []

@app.get('/movies/', tags=["Movies"])
def get_movie_by_category(category: str, year: int) -> Movie:
    for movie in movies:
        if movie['category'] == category:
            return movie.model_dump()
    return []

@app.post("/movies", tags=["Movies"])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    return [movie.model_dump() for movie in movies]

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
            return [movie.model_dump() for movie in movies]
    return []
    
    
@app.delete('/movies/{id}', tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return [movie.model_dump() for movie in movies]
