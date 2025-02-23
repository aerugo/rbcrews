from typing import Protocol, runtime_checkable

import fitz  # type: ignore
from pydantic import BaseModel


###############################################################################
# Pydantic Data Models
###############################################################################
class PdfReport(BaseModel):
    """Represents a single PDF file stored in memory."""
    filename: str
    content_text: str

###############################################################################
# Repository Protocol
###############################################################################
@runtime_checkable
class PdfRepository(Protocol):
    """Interface for storing and retrieving PDF reports in memory."""
    def store_pdf(self, pdf: PdfReport) -> None: ...
    def list_pdfs(self) -> list[PdfReport]: ...
    def clear(self) -> None: ...

###############################################################################
# In-Memory Implementation
###############################################################################
class InMemoryPdfRepo:
    """Trivial in-memory repository for PDF data."""
    def __init__(self) -> None:
        self._storage: dict[str, PdfReport] = {}

    def store_pdf(self, pdf: PdfReport) -> None:
        self._storage[pdf.filename] = pdf

    def list_pdfs(self) -> list[PdfReport]:
        return list(self._storage.values())

    def clear(self) -> None:
        self._storage.clear()

###############################################################################
# PDF Parsing
###############################################################################
def parse_pdf(pdf_content: bytes) -> str:
    """
    Extract text from PDF content using PyMuPDF.
    Returns the full text content from all pages.
    """
    try:
        # Open the PDF from the given byte stream
        doc = fitz.open("pdf", pdf_content)
    except Exception as e:
        return f"Error opening PDF: {e}"

    text: str = ""
    # Extract text from each page
    for page in doc:
        text += page.get_text("text")  # type: ignore
    doc.close()
    assert isinstance(text, str)
    return text