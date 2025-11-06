from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import (
    PlainTextResponse,
    JSONResponse,
    Response
)
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler


# pydantic es para manejo de errores
app = FastAPI()


# app.add_middleware(HTTPErrorHandler)
@app.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    print("Middleware activated")
    return await call_next(request)

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content="Home", status_code=200)

app.include_router(prefix='/movies', router=movie_router)
