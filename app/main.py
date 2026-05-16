import os
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.csv_loader import load_students_from_csv
from app.csv_writer import write_pairings_to_csv
from app.database import get_facilitators, init_db, save_facilitators
from app.pairing_logic import generate_pairings


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(lifespan=lifespan)
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
async def upload_csv(request: Request,file: UploadFile = File(...), overlap_weight: int = Form(...), experience_weight: int = Form(...), confidence_weight: int = Form(...)):

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    upload_path = f"uploads/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load students
    students = load_students_from_csv(upload_path)
    save_facilitators(students)

    weights = {
        "overlap": overlap_weight,
        "experience": experience_weight,
        "confidence": confidence_weight
    }
    # Generate pairings
    pairings = generate_pairings(students, weights)

    global latest_pairings
    latest_pairings = pairings

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={"pairings": pairings}
    )


@app.get("/facilitators")
def facilitators():

    return {
        "facilitators": get_facilitators()
    }


@app.get("/download")
def download_pairings():

    output_path = "output/pairings_output.csv"

    write_pairings_to_csv(latest_pairings, output_path)

    return FileResponse(
        output_path,
        media_type="text/csv",
        filename="pairings_output.csv"
    )
