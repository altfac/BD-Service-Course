from fastapi import UploadFile
from auth import *

education_router = APIRouter()
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
            file = open("../templates/" + i[2], "r+")
            i[2] = file.read()
            file.close()

    params = {"request": request, "chapter": chapter, "current": "Chapter"}
    return templates.TemplateResponse("html/education/chapter.html", params, media_type="text/html")


@education_router.get("/delete_material/{chapter_id}/{material_id}")
async def delete_education_material(request: Request, chapter_id: int, material_id: int):
    if not check_auth(request):
        return login(request)

    my_database.delete_education_material(chapter_id, material_id)

    return RedirectResponse(f"/chapter/{chapter_id}")


@education_router.get("/delete_chapter/{id}")
async def delete_chapter(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    my_database.delete_chapter(id)

    return RedirectResponse(f"/theory_chapters_edit")


@education_router.get("/add_chapter/{course}/{level}")
async def add_chapter(request: Request, course: str, level: str, name: str):
    if not check_auth(request):
        return login(request)

    my_database.add_chapter(course, level, name, get_admin_id(request))

    return RedirectResponse(f"/theory_chapters_edit")


@education_router.post("/add_material/{id}")
async def add_material(request: Request, file: UploadFile, id: int, type: str = Form(None)):
    if not check_auth(request):
        return login(request)

    if file.filename:
        up_file = open("../templates/files/" + file.filename, "wb+")
        up_file.write(file.file.read())
        file.file.close()
        up_file.close()

    my_database.add_material(id, type, "files/" + file.filename)

    return RedirectResponse(f"/chapter/{id}", status_code=303)


@education_router.get("/add_course")
async def add_course(request: Request, name: str):
    if not check_auth(request):
        return login(request)

    my_database.add_course(name)

    return RedirectResponse(f"/theory_chapters_edit")
