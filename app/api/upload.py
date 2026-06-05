from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import APIRouter
from fastapi import Request
from pathlib import Path
from app.services.pdf_service import extract_text_from_pdf
from app.agents.extraction_agent import extract_bank_details
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.services.chunking_serrvice import chunk_text_by_lines
from app.services.merge_metrics import merge_monthly_metrics

MAX_FILE_SIZE = 10 * 1024 * 1024  # 5 MB

UPLOAD_DIR = "app/documents"

Path(UPLOAD_DIR).mkdir(exist_ok = True)

router = APIRouter()

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)
    
    chunks = chunk_text_by_lines(text, rows_per_chunk=50)

    all_chunk_transactions = []

    for index, chunk in enumerate(chunks):

        print(f"Processing chunk {index + 1}")

        metrics = extract_bank_details(chunk)
        all_chunk_transactions.append(metrics)


    merged_metrics = merge_monthly_metrics(all_chunk_transactions)

    return {
        "monthly_summary": merged_metrics
    }