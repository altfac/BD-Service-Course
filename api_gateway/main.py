import datetime
from fastapi import FastAPI, Request, Response, Form, Cookie, UploadFile
from fastapi.responses import JSONResponse
import requests
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from database import *

SECRET_KEY = "09d25e094faa9154613450832486f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


app = FastAPI(title="Curse", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")
connection = mysql.connector.connect(host="localhost", user="root", password="root", database="curseusers")
my_database = Datebase(connection)
my_database.get_all_education_materials()


def check_auth():
    return True


def auth():
    pass


@app.get("/")
async def auth(request: Request):
    if not check_auth():
        return auth()

    params = {"request": request}
    return templates.TemplateResponse("html/main.html", params, media_type="text/html")


@app.get("/theory_tasks_edit")
async def theory_tasks_edit(request: Request):
    global my_database

    if not check_auth():
        return auth()

    params = {"request": request, "task": my_database.get_all_education_materials(), "current": "Theory tasks edit"}
    return templates.TemplateResponse("html/theory_tasks.html", params, media_type="text/html")


@app.get("/practical_tasks_edit")
async def practical_tasks_edit(request: Request):
    global my_database

    if not check_auth():
        return auth()

    params = {"request": request, "task": {}, "current": "Practical tasks edit"}
    return templates.TemplateResponse("html/practical_tasks.html", params, media_type="text/html")


@app.get("/users_edit")
async def users_edit(request: Request):
    global my_database

    if not check_auth():
        return auth()

    params = {"request": request, "task": {}, "current": "User edit"}
    return templates.TemplateResponse("html/users.html", params, media_type="text/html")


@app.get("/task/{id}")
async def get_task(request: Request, id: int):
    global my_database

    if not check_auth():
        return auth()

    task = my_database.get_education_material(id)
    if not task:
        return RedirectResponse("/")
    for i in task[2]:
        if i[1] == "Текст":
            file = open("../templates/" + i[2], "r+")
            i[2] = file.read()
            file.close()

    params = {"request": request, "task": task, "current": "Task"}
    return templates.TemplateResponse("html/task.html", params, media_type="text/html")


@app.get("/delete_material/{task_id}/{material_id}")
async def delete_education_material(request: Request, task_id: int, material_id: int):
    global my_database

    if not check_auth():
        return auth()

    my_database.delete_education_material(task_id, material_id)

    return RedirectResponse(f"/task/{task_id}")


@app.get("/delete_task/{id}")
async def delete_task(request: Request, id: int):
    global my_database

    if not check_auth():
        return auth()

    my_database.delete_task(id)

    return RedirectResponse(f"/theory_tasks_edit")


@app.post("/add_material/{id}")
async def delete_task(file: UploadFile, id: int, type: str = Form(None)):
    global my_database

    if not check_auth():
        return auth()

    if file.filename:
        up_file = open("../templates/task_files/" + file.filename, "wb+")
        up_file.write(file.file.read())
        file.file.close()
        up_file.close()

    my_database.add_material(id, type, "task_files/" + file.filename)

    return RedirectResponse(f"/task/{id}", status_code=303)


@app.get("/add_task/{course}/{level}")
async def add_task(request: Request, course: str, level: str, name: str):
    global my_database

    if not check_auth():
        return auth()

    my_database.add_task(course, level, name)

    return RedirectResponse(f"/theory_tasks_edit")


app.mount("/css", StaticFiles(directory="../templates/css"), "css")
app.mount("/task_files", StaticFiles(directory="../templates/task_files"), "task_files")