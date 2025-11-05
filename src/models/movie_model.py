import datetime
from pydantic import BaseModel, Field

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
