from fastapi import FastAPI, Depends, Header, Request, Response
from fastapi.params import Query
from fastapi.requests import Request
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from typing import Annotated
from fastapi.exceptions import HTTPException
from jose import jwt


def dependecy1():
    print("Ejecutando dependencia 1")


def dependency2():
    print("Ejecutando dependencia 2")


app = FastAPI(dependencies=[Depends(dependecy1), Depends(dependency2)])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users = {
    "pablo": {"username": "pablo", "password": "1234", "email": "pab@gmail.com"},
    "juan": {"username": "juan", "password": "abcd", "email": "user@gmail.com"},
}

app.add_middleware(HTTPErrorHandler)


static_path = os.path.join(os.path.dirname(__file__), "static/")
templates_path = os.path.join(os.path.dirname(__file__), "templates/")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

app.title = "Mi primera API con FastAPI"
app.version = "2.0.0"


class CommonDep:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date


def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, "my-secret", algorithm="HS256")
    return token


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    user = user.get(data["username"])
    return user


@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/profile")
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user


@app.get("/", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Hello World",
        },
    )


def get_headers(
    access_token: Annotated[str | None, Header()] = None,
    user_role: Annotated[str | None, Header()] = None,
):
    if access_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid access token")
    return {"access_token": access_token, "user_role": user_role}


@app.get("/dashboard")
def dashboard(headers: Annotated[dict, Depends(get_headers)]):
    return {"access_token": headers["access_token"], "user_role": headers["user_role"]}


@app.get("/users")
def get_users(commons: CommonDep = Depends()):
    return f"Users created between {commons.start_date} and {commons.end_date}"


@app.get("/customers")
def get_customers(commons: CommonDep = Depends()):
    return f"Customers created between {commons.start_date} and {commons.end_date}"


app.include_router(prefix="/movies", router=movie_router)
