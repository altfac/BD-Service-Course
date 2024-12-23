from starlette.staticfiles import StaticFiles
from auth import *
from auth import auth_router
from education_tasks import education_router
from practical_tasks import practical_router

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


@app.get("/top")
async def top(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "users": my_database.get_top()}
    return templates.TemplateResponse("html/top.html", params, media_type="text/html")


@app.exception_handler(404)
async def unicorn_exception_handler(request: Request, exc):
    params = {"request": request, "current": "Exception", "exception": exc}

    return templates.TemplateResponse("html/exception.html", params)


@app.exception_handler(405)
async def unicorn_exception_handler(request: Request, exc):
    params = {"request": request, "current": "Exception", "exception": exc}

    return templates.TemplateResponse("html/exception.html", params)


app.include_router(education_router)
app.include_router(practical_router)
app.include_router(auth_router)
app.mount("/css", StaticFiles(directory="../templates/css"), "css")
app.mount("/files", StaticFiles(directory="../templates/files"), "files")