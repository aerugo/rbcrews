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
