from starlette.staticfiles import StaticFiles
from student_part.auth import *


practical_router = FastAPI(title="Course", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")


@practical_router.get("/practical_tasks_edit")
async def practical_tasks_edit(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "task": my_database.get_all_practical_tasks(), "current": "Practical tasks edit"}
    return templates.TemplateResponse("html/practical/practical_tasks.html", params, media_type="text/html")


@practical_router.get("/practical_task/{id}")
async def get_task(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "task": my_database.get_practical_task(id),
              "attempts": my_database.get_all_attempts_of_task(id, get_student_id(request)), "current": "Task"}
    return templates.TemplateResponse("html/practical/task.html", params, media_type="text/html")


@practical_router.get("/add_attempt/{id}")
async def add_attempt(request: Request, id: int, answer: str):
    if not check_auth(request):
        return login(request)

    my_database.add_attempt(id, get_student_id(request), answer)

    return RedirectResponse(f"/practical_task/{id}", status_code=303)


practical_router.mount("/css", StaticFiles(directory="../templates/css"), "css")
practical_router.mount("/files", StaticFiles(directory="../../files"), "files")
