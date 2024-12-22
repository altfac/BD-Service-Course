import datetime
from fastapi import FastAPI, Request, Response, Form, Cookie, UploadFile
from fastapi.responses import JSONResponse
import requests
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from database import *
from auth import *
from education_tasks import education_router
from practical_tasks import practical_router

SECRET_KEY = "09d25e094faa9154613450832486f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


app = FastAPI(title="Curse", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")
connection = mysql.connector.connect(host="localhost", user="root", password="root", database="curseusers")
my_database = Datebase(connection)


@app.get("/")
async def auth(request: Request):
    if not check_auth():
        return auth()

    params = {"request": request}
    return templates.TemplateResponse("html/main.html", params, media_type="text/html")


@app.get("/users_edit")
async def users_edit(request: Request):
    global my_database

    if not check_auth():
        return auth()

    params = {"request": request, "task": {}, "current": "User edit"}
    return templates.TemplateResponse("html/users.html", params, media_type="text/html")


@app.exception_handler(404)
async def unicorn_exception_handler(request: Request, exc):
    params = {"request": request, "current": "Exception", "exception": exc}

    return templates.TemplateResponse("html/exception.html", params)


app.include_router(education_router)
app.include_router(practical_router)
app.mount("/css", StaticFiles(directory="../templates/css"), "css")
app.mount("/files", StaticFiles(directory="../templates/files"), "files")