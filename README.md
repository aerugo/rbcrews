# rbcrew

A minimal example demonstrating a multimodal financial report summarizer and comparator API. This project uses Python 3.13, Pydantic 2.x, FastAPI, and CrewAI.

## Prerequisites

- Python 3.13 installed
- [uv package manager](https://pypi.org/project/uv/) installed

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/rbcrew.git
   cd rbcrew
   ```

2. **Install dependencies with uv:**

   ```bash
   uv sync
   ```

   This command will install all required packages as specified in `pyproject.toml`.


Run the server with uvicorn:

```bash
uv uvicorn app:app --reload
```

Then, open your browser and visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the PDF uploader interface.

## Usage

1. **Upload PDFs:** Use the web form at the root URL (`/`) to upload one or more PDF reports.
2. **Process PDFs:** Call the `/process` endpoint to run summarization on each uploaded PDF and generate a comparison report.
4. **Clear Data:** Use the `/clear` endpoint to remove all stored PDFs and results.
