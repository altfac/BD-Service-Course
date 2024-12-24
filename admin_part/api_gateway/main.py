from fastapi import FastAPI, UploadFile
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from admin_part.auth import *
from admin_part.auth import auth_router
from admin_part.user_microservice.users import users_router
from admin_part.education_microservice.education_tasks import education_router
from admin_part.practical_microservice.practical_tasks import practical_router
import requests

app = FastAPI(title="Course", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")


@app.get("/")
async def main(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "user": my_database.get_admin(get_admin_id(request))}
    return templates.TemplateResponse("html/main.html", params, media_type="text/html")


@app.get("/theory_chapters_edit")
async def chapter_edit(request: Request):
    return HTMLResponse(content=requests.get("http://127.0.0.4:8003/theory_chapters_edit",
                                             cookies=request.cookies).content)


@app.get("/chapter/{id}")
async def get_chapter(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.4:8003/chapter/{id}",
                                             cookies=request.cookies).content)


@app.get("/delete_material/{chapter_id}/{material_id}")
async def delete_education_material(request: Request, chapter_id: int, material_id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.4:8003/delete_material/{chapter_id}/{material_id}",
                                             cookies=request.cookies).content)


@app.get("/delete_chapter/{id}")
async def delete_chapter(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.4:8003/delete_chapter/{id}",
                                             cookies=request.cookies).content)


@app.get("/add_chapter/{course}/{level}")
async def add_chapter(request: Request, course: str, level: str, name: str):
    return HTMLResponse(content=requests.get(f"http://127.0.0.4:8003/add_chapter/{course}/{level}",
                                             params={"course": course, "name": name, "level": level},
                                             cookies=request.cookies).content)


@app.post("/add_material/{id}")
async def add_material(request: Request, file: UploadFile, id: int, type: str = Form(None)):
    return HTMLResponse(content=requests.post(f"http://127.0.0.4:8003/add_material/{id}",
                                              params={"type": type}, files={"file": file.file},
                                              cookies=request.cookies).content)


@app.get("/add_course/{id}")
async def add_course(request: Request, name: str, id: int):
    content = requests.get(f"http://127.0.0.4:8003/add_course",
                           params={"name": name},
                           cookies=request.cookies).content
    if "\"added\"".encode('utf-8') != content:
        return HTMLResponse(content=content)
    if id == 0:
        return RedirectResponse(f"/theory_chapters_edit")
    else:
        return RedirectResponse(f"/practical_tasks_edit")


@app.get("/practical_tasks_edit")
async def practical_tasks_edit(request: Request):
    return HTMLResponse(content=requests.get(f"http://127.0.0.5:8004/practical_tasks_edit",
                                             cookies=request.cookies).content)


@app.get("/practical_task/{id}")
async def get_task(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.5:8004/practical_task/{id}",
                                             cookies=request.cookies).content)


@app.get("/update_task/{id}")
async def update_task(request: Request, id: int, name: str, description: str, reward: int, answer: str):
    return HTMLResponse(content=requests.get(f"http://127.0.0.5:8004/update_task/{id}",
                                             params={"name": name, "description": description,
                                                     "reward": reward, "answer": answer},
                                             cookies=request.cookies).content)


@app.get("/delete_practical_task/{id}")
async def delete_task(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.5:8004/delete_practical_task/{id}",
                                             cookies=request.cookies).content)


@app.get("/add_practical_task/{course}/{level}")
async def add_chapter(request: Request, course: str, level: str, name: str, description: str, reward: int, answer: str):
    return HTMLResponse(content=requests.get(f"http://127.0.0.5:8004/add_practical_task/{course}/{level}",
                                             params={"name": name, "description": description,
                                                     "reward": reward, "answer": answer},
                                             cookies=request.cookies).content)


@app.get("/users_edit")
async def users_edit(request: Request):
    return HTMLResponse(content=requests.get(f"http://127.0.0.6:8005/users_edit",
                                             cookies=request.cookies).content)


@app.get("/delete_student/{id}")
async def delete_student(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.6:8005/delete_student/{id}",
                                             cookies=request.cookies).content)


@app.get("/edit_student/{id}")
async def edit_student(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.6:8005/edit_student/{id}",
                                             cookies=request.cookies).content)


@app.get("/update_student/{id}")
async def update_student(request: Request, id: int, name: str, email: str):
    return HTMLResponse(content=requests.get(f"http://127.0.0.6:8005/update_student/{id}",
                                             params={"name": name, "email": email},
                                             cookies=request.cookies).content)


@app.post("/add_student")
async def add_student(request: Request, name: str = Form(None), email: str = Form(None), password: str = Form(None)):
    return HTMLResponse(content=requests.post(f"http://127.0.0.6:8005/add_student",
                                              params={"name": name, "email": email, "password": password},
                                              cookies=request.cookies).content)


@app.post("/add_admin")
async def add_student(request: Request, name: str = Form(None), email: str = Form(None),
                      password: str = Form(None), role: int = Form(None)):
    return HTMLResponse(content=requests.post(f"http://127.0.0.6:8005/add_admin",
                                              params={"name": name, "email": email,
                                                      "password": password, "role": role},
                                              cookies=request.cookies).content)


@app.get("/edit_admin/{id}")
async def edit_admin(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.6:8005/edit_admin/{id}",
                                             cookies=request.cookies).content)


@app.get("/update_admin/{id}")
async def update_admin(request: Request, id: int, name: str, email: str, role: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.6:8005/update_admin/{id}",
                                             params={"name": name, "email": email, "role": role},
                                             cookies=request.cookies).content)


@app.exception_handler(404)
async def unicorn_exception_handler(request: Request, exc):
    params = {"request": request, "current": "Exception", "exception": exc}

    return templates.TemplateResponse("html/exception.html", params)


@app.exception_handler(405)
async def unicorn_exception_handler(request: Request, exc):
    params = {"request": request, "current": "Exception", "exception": exc}

    return templates.TemplateResponse("html/exception.html", params)


app.include_router(auth_router)
app.mount("/css", StaticFiles(directory="../templates/css"), "css")
app.mount("/files", StaticFiles(directory="../../files"), "files")
