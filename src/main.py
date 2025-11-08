from fastapi import FastAPI, Depends
from fastapi.params import Query
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, JSONResponse, Response
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

def dependecy1():
    print("Ejecutando dependencia 1")
    
def dependency2():
    print("Ejecutando dependencia 2")
app = FastAPI(dependencies=[Depends(dependecy1), Depends(dependency2)])


app.add_middleware(HTTPErrorHandler)

static_path = os.path.join(os.path.dirname(__file__), "static/")
templates_path = os.path.join(os.path.dirname(__file__), "templates/")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"

# def common_params(start_date: str, end_date: str):
#     return { "start_date": start_date, "end_date": end_date}

# CommonDep = Annotated[dict, Depends(common_params)]


class CommonDep:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date


@app.get("/", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Hello World",
        },
    )


@app.get("/users")
def get_users(commons: CommonDep = Depends()):
    return f"Users created between {commons.start_date} and {commons.end_date}"


@app.get("/customers")
def get_customers(commons: CommonDep = Depends()):
    return (
        f"Customers created between {commons.start_date} and {commons.end_date}"
    )


app.include_router(prefix="/movies", router=movie_router)
