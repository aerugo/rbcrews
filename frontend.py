from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

async def frontend(request: Request) -> HTMLResponse:
    """
    Render the frontend template for PDF upload and processing.
    """
    return templates.TemplateResponse("frontend.html", {"request": request})
