from fastapi import APIRouter, FastAPI, Request, Response, Form, Cookie, UploadFile
from database import *
from auth import *
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


practical_router = APIRouter()
templates = Jinja2Templates(directory="../templates")
connection = mysql.connector.connect(host="localhost", user="root", password="root", database="curseusers")
my_database = Datebase(connection)


@practical_router.get("/practical_tasks_edit")
async def practical_tasks_edit(request: Request):
    global my_database

    if not check_auth():
        return auth()

    params = {"request": request, "task": my_database.get_all_education_materials(), "current": "Practical tasks edit"}
    return templates.TemplateResponse("html/practical_tasks.html", params, media_type="text/html")


