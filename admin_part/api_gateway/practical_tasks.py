from auth import *
practical_router = APIRouter()
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

    params = {"request": request, "task": my_database.get_practical_task(id), "current": "Task"}
    return templates.TemplateResponse("html/practical/task.html", params, media_type="text/html")


@practical_router.get("/update_task/{id}")
async def update_task(request: Request, id: int, name: str, description: str, reward: int, answer: str):
    if not check_auth(request):
        return login(request)

    if not my_database.update_practical_task(id, name, description, reward, answer):
        return RedirectResponse("/practical_tasks_edit", status_code=303)

    return RedirectResponse(f"/practical_task/{id}", status_code=303)


@practical_router.get("/delete_practical_task/{id}")
async def delete_task(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    my_database.delete_practical_task(id)

    return RedirectResponse(f"/practical_tasks_edit")


@practical_router.get("/add_practical_task/{course}/{level}")
async def add_chapter(request: Request, course: str, level: str, name: str, description: str, reward: int, answer: str):
    if not check_auth(request):
        return login(request)

    my_database.add_practical_task(course, level, name, description, reward, answer, get_admin_id(request))

    return RedirectResponse(f"/practical_tasks_edit")