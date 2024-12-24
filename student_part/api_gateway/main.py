import requests
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from student_part.auth import *
from student_part.auth import auth_router
from student_part.education_microservice.education_tasks import education_router
from student_part.practical_mircoservice.practical_tasks import practical_router

app = FastAPI(title="Course", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")


@app.get("/")
async def main(request: Request):
    if not check_auth(request):
        return login(request)

    student_id = get_student_id(request)
    params = {"request": request, "user": my_database.get_student(student_id),
              "rating": my_database.get_student_rating(student_id)}
    return templates.TemplateResponse("html/main.html", params, media_type="text/html")


@app.get("/theory_chapters_edit")
async def chapter_edit(request: Request):
    return HTMLResponse(content=requests.get("http://127.0.0.8:8007/theory_chapters_edit",
                                             cookies=request.cookies).content)


@app.get("/chapter/{id}")
async def get_chapter(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.8:8007/chapter/{id}",
                                             cookies=request.cookies).content)


@app.get("/practical_task/{id}")
async def get_task(request: Request, id: int):
    return HTMLResponse(content=requests.get(f"http://127.0.0.9:8008/practical_task/{id}",
                                             cookies=request.cookies).content)


@app.get("/add_attempt/{id}")
async def add_attempt(request: Request, id: int, answer: str):
    return HTMLResponse(content=requests.get(f"http://127.0.0.9:8008/add_attempt/{id}",
                                             params={"answer": answer},
                                             cookies=request.cookies).content)


@app.get("/practical_tasks_edit")
async def practical_tasks_edit(request: Request):
    return HTMLResponse(content=requests.get(f"http://127.0.0.9:8008/chapter",
                                             cookies=request.cookies).content)


@app.get("/top")
async def top(request: Request):
    return HTMLResponse(content=requests.get(f"http://127.0.0.10:8009/top",
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