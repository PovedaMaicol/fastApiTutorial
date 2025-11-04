import datetime
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
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
        "json_schema_extra": {
            "example": {
                "id": 3,
                "title": "Movie Example",
                "overview": "This is an example overview for a movie.",
                "year": 2023,
                "rating": 8.5,
                "category": "Drama",
            }
        }
    }


movies: List[Movie] = []

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


@app.get("/", tags=["Home"])
def home():
    return PlainTextResponse(content="Home", status_code=200)


@app.get("/movies", tags=["Movies"], status_code=200, response_description='Nos debe devolver una respuesta exitosa')
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int = Path(ge=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


@app.get("/movies/", tags=["Movies"])
def get_movie_by_category(
    category: str = Query(min_length=5, max_length=20)
) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


@app.post("/movies", tags=["Movies"])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content, status_code=201)
    # return RedirectResponse('/movies', status_code=303)


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
            content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.get("/get_file")
def get_file():
    return FileResponse('uneee.pdf')
