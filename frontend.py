from fastapi.responses import HTMLResponse


async def frontend() -> HTMLResponse:
    """
    Very simple HTML form to upload PDFs. For production, use a real template
    system or a more sophisticated frontend.
    """
    html_content = """
    <html>
      <head><title>PDF Uploader</title></head>
      <body>
        <h1>Upload Central Bank PDF Reports</h1>
        <form id="upload-form" action="/upload" method="post" enctype="multipart/form-data">
          <input type="file" name="pdf_files" multiple>
          <button type="submit">Upload PDFs</button>
        </form>
        <div id="upload-message" style="margin-top: 10px;"></div>
        <hr/>
        <h2>Run Summaries</h2>
        <p>After uploading PDFs, call <code>/process</code> to summarize and compare them.</p>
        <p>Check <code>/summaries</code> to see individual summaries, and <code>/comparison</code> for the changes report.</p>
        <form action="/process" method="get">
          <button type="submit">Process PDFs</button>
        </form>
        <script>
          document.getElementById("upload-form").addEventListener("submit", async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const response = await fetch("/upload", {
              method: "POST",
              body: formData
            });
            const result = await response.json();
            document.getElementById("upload-message").innerText = result.message;
          });
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)