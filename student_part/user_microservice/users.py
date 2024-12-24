from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from admin_part.auth import *

users_router = FastAPI(title="Course", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")


@users_router.get("/top")
async def top(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "users": my_database.get_top()}
    return templates.TemplateResponse("html/top.html", params, media_type="text/html")


users_router.mount("/css", StaticFiles(directory="../templates/css"), "css")
users_router.mount("/files", StaticFiles(directory="../../files"), "files")
