"""
====================================================
Multimodal Financial Report Summarizer and Comparator
====================================================

A minimal example demonstrating how to:

1. Provide an API endpoint for uploading multiple PDF reports.
2. Use a CrewAI crew of experts to:
    - Summarize each PDF with a macroeconomic and inflation focus.
    - Compare these summaries and create a "changes report" highlighting differences.

Usage:
    1. Run server:  uvicorn app:app --reload
    2. Visit http://127.0.0.1:8000 to upload PDFs
    3. Then call GET /process to run the summarization and comparison
    4. Retrieve results at GET /summaries or GET /comparison

====================================================
Following the Style Conventions
====================================================
"""

import asyncio

import markdown
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

from crew import FullCrew, compare_summaries, summarize_one_pdf
from frontend import frontend
from pdf import InMemoryPdfRepo, PdfReport, parse_pdf

# Initialize the FastAPI app
app = FastAPI()

# Simple in-memory store for PDFs
repo = InMemoryPdfRepo()

# Instantiate the full crew
full_crew = FullCrew()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return await frontend()

@app.post("/upload")
async def upload_pdfs(pdf_files: list[UploadFile]):
    """
    Accept an arbitrary number of PDF files and store them in memory.
    """
    repo.clear()
    for file in pdf_files:
        content = await file.read()
        assert isinstance(file.filename, str)
        text = parse_pdf(content)
        assert isinstance(text, str)
        new_pdf = PdfReport(filename=file.filename, content_text=text)
        repo.store_pdf(new_pdf)
    return {"message": f"Uploaded {len(pdf_files)} PDF(s) successfully."}

@app.get("/process")
async def process_reports():
    """Stream PDF processing results in real-time."""
    pdfs = repo.list_pdfs()
    if not pdfs:
        async def no_pdf():
            yield markdown.markdown("Error: No PDFs to process.\n")
        return StreamingResponse(no_pdf(), media_type="text/html")

    async def event_generator():
        yield markdown.markdown("Starting processing of PDFs...\n\n---\n")
        print("Starting processing of PDFs...")
        # Create an async task per PDF along with its filename
        tasks: list[asyncio.Task[str]] = [
            asyncio.create_task(
                summarize_one_pdf(filename=pdf.filename, pdf_content=pdf.content_text)
            )
            for pdf in pdfs
        ]

        # To preserve association, build a list of tuples (filename, task)
        tasks_with_names = list(zip([pdf.filename for pdf in pdfs], tasks))
        completed_summaries: list[str] = []

        # As each task completes, yield its result
        for i, future in enumerate(asyncio.as_completed([t for _, t in tasks_with_names]), start=1):
            summary_text = await future
            completed_summaries.append(summary_text)
            line = f"PDF #{i}: \n\n{summary_text}\n"
            print(summary_text)
            yield markdown.markdown(f"{line}\n---\n")

        # After all summarizations, start the comparison stage
        yield markdown.markdown("Starting comparison of summaries...\n\n---\n")
        print("Starting comparison of summaries...")
        comparison_report = await compare_summaries(completed_summaries)
        print(comparison_report)
        yield markdown.markdown(f"{comparison_report}\n---\n")

    return StreamingResponse(event_generator(), media_type="text/html")