from starlette.staticfiles import StaticFiles
from student_part.auth import *

education_router = FastAPI(title="Course", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")


@education_router.get("/theory_chapters_edit")
async def chapter_edit(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "chapter": my_database.get_all_education_materials(), "current": "Theory chapter edit"}
    return templates.TemplateResponse("html/education/theory_chapters.html", params, media_type="text/html")


@education_router.get("/chapter/{id}")
async def get_chapter(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    chapter = my_database.get_education_material(id)
    if not chapter:
        return RedirectResponse("/")
    for i in chapter[2]:
        if i[1] == "Текст":
            file = open("../../" + i[2], "r+")
            i[2] = file.read()
            file.close()

    params = {"request": request, "chapter": chapter, "current": "Chapter"}
    return templates.TemplateResponse("html/education/chapter.html", params, media_type="text/html")


education_router.mount("/css", StaticFiles(directory="../templates/css"), "css")
education_router.mount("/files", StaticFiles(directory="../../files"), "files")
