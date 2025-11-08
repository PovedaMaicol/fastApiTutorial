from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import (
    PlainTextResponse,
    JSONResponse,
    Response
)
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()


app.add_middleware(HTTPErrorHandler)

static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

app.mount('/static', StaticFiles(directory=static_path), name='static')
templates = Jinja2Templates(directory=templates_path)

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


@app.get('/', tags=['Home'])
def home(request: Request):
    return templates.TemplateResponse('index.html', { 'request': request, 'message': 'Hello World', })

app.include_router(prefix='/movies', router=movie_router)
