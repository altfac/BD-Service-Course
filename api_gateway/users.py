from auth import *

users_router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@users_router.get("/users_edit")
async def users_edit(request: Request):
    if not check_auth(request):
        return login(request)

    users = my_database.get_all_users()
    if not users:
        return RedirectResponse("/", status_code=303)

    params = {"request": request, "users": users, "current": "User edit"}
    return templates.TemplateResponse("html/users/all_users.html", params, media_type="text/html")


@users_router.get("/delete_student/{id}")
async def delete_student(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    if get_admin_permission(request) < 1:
        return RedirectResponse("/", status_code=303)

    my_database.delete_student(id)

    return RedirectResponse("/users_edit", status_code=303)


@users_router.get("/edit_student/{id}")
async def edit_student(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    student = my_database.get_student(id)

    if get_admin_permission(request) < 1 or not student:
        return RedirectResponse("/", status_code=303)

    params = {"request": request, "student": student, "current": "Student edit"}
    return templates.TemplateResponse("html/users/student_edit.html", params, media_type="text/html")


@users_router.get("/update_student/{id}")
async def update_student(request: Request, id: int, name: str, email: str):
    if not check_auth(request):
        return login(request)

    if get_admin_permission(request) < 1:
        return RedirectResponse("/", status_code=303)

    my_database.update_student(id, name, email)

    return RedirectResponse(f"/edit_student/{id}", status_code=303)


@users_router.post("/add_student")
async def add_student(request: Request, name: str = Form(None), email: str = Form(None), password: str = Form(None)):
    if not check_auth(request):
        return login(request)

    if get_admin_permission(request) < 1:
        return RedirectResponse("/", status_code=303)

    password = hashlib.sha256(password.encode()).hexdigest()

    my_database.add_student(name, email, password)

    return RedirectResponse("/users_edit", status_code=303)


@users_router.post("/add_admin")
async def add_student(request: Request, name: str = Form(None), email: str = Form(None),
                      password: str = Form(None), role: int = Form(None)):
    if not check_auth(request):
        return login(request)

    if get_admin_permission(request) < 2:
        return RedirectResponse("/", status_code=303)

    password = hashlib.sha256(password.encode()).hexdigest()
    my_database.add_admin(name, email, password, role)

    return RedirectResponse("/users_edit", status_code=303)


@users_router.get("/edit_admin/{id}")
async def edit_student(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    admin = my_database.get_admin(id)

    if get_admin_permission(request) < 2 or not admin:
        return RedirectResponse("/", status_code=303)

    params = {"request": request, "admin": admin, "current": "Admin edit"}
    return templates.TemplateResponse("html/users/admin_edit.html", params, media_type="text/html")


@users_router.get("/update_admin/{id}")
async def update_admin(request: Request, id: int, name: str, email: str, role: int):
    if not check_auth(request):
        return login(request)

    if get_admin_permission(request) < 2:
        return RedirectResponse("/", status_code=303)

    my_database.update_admin(id, name, email, role)

    return RedirectResponse(f"/edit_admin/{id}", status_code=303)