from fastapi import APIRouter,Request, Form
from starlette.responses import HTMLResponse

from models.note import Note
from config.db import conn
from schemas.note import NoteEntity,Notesentity
from fastapi.templating import Jinja2Templates


note=APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/",response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc.get("title", "No Title"),
            "desc": doc.get("desc", "No Description"),
        })
    return templates.TemplateResponse(name="index.html", context={"request": request, "newDocs": newDocs})

@note.post("/")
async def create_note(title: str = Form(...), desc: str = Form(...)):
    note_data = {"title": title, "desc": desc}
    # print("Received Form Data:", note_data)
    result = conn.notes.notes.insert_one(note_data)
    return {"message": "Note created successfully", "id": str(result.inserted_id)}