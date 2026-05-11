import os
import shutil

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.csv_loader import load_students_from_csv
from app.csv_writer import write_pairings_to_csv
from app.pairing_logic import generate_pairings


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

latest_pairings = []


@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/upload")
async def upload_csv(request: Request,file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    upload_path = f"uploads/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load students
    students = load_students_from_csv(upload_path)

    # Generate pairings
    pairings = generate_pairings(students)

    global latest_pairings
    latest_pairings = pairings

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={"pairings": pairings}
    )

@app.get("/download")
def download_pairings():

    output_path = "output/pairings_output.csv"

    write_pairings_to_csv(latest_pairings, output_path)

    return FileResponse(
        output_path,
        media_type="text/csv",
        filename="pairings_output.csv"
    )