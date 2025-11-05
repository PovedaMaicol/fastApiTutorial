from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import (
    PlainTextResponse
)
from src.routers.movie_router import movie_router


# pydantic es para manejo de errores
app = FastAPI()



app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content="Home", status_code=200)

app.include_router(prefix='/movies', router=movie_router)
