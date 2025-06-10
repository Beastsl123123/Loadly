import os
from flask import Flask, render_template_string, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Upload File</title>
  <style>
    body {
      font-family: "Inter", sans-serif;
      background: #fff;
      color: #6b7280;
      margin: 0;
      padding: 2rem;
      display: flex;
      justify-content: center;
    }
    .container {
      max-width: 600px;
      width: 100%;
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 0 6px rgba(0,0,0,0.05);
    }
    h1 {
      font-weight: 700;
      font-size: 3rem;
      margin-bottom: 1.5rem;
      color: #111827;
    }
    form {
      display: flex;
      gap: 1rem;
      margin-bottom: 2rem;
    }
    input[type="file"] {
      flex-grow: 1;
      font-size: 1rem;
      border: 1px solid #d1d5db;
      border-radius: 8px;
      padding: 0.5rem;
    }
    input[type="submit"] {
      background: #111827;
      color: white;
      border: none;
      border-radius: 8px;
      padding: 0.5rem 1.5rem;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.25s ease;
    }
    input[type="submit"]:hover,
    input[type="submit"]:focus {
      background: #374151;
      outline: none;
    }
    pre {
      background: #f9fafb;
      padding: 1rem;
      border-radius: 8px;
      overflow-x: auto;
      white-space: pre-wrap;
      color: #374151;
      font-size: 1rem;
      max-height: 300px;
    }
    .message {
      background: #fffbeb;
      color: #854d0e;
      padding: 1rem;
      border-radius: 8px;
      font-size: 1rem;
    }
  </style>
</head>
<body>
  <div class="container" role="main">
    <h1>Upload File</h1>
    <form method="POST" enctype="multipart/form-data" aria-label="File Upload Form">
      <input type="file" name="file" required aria-required="true" />
      <input type="submit" value="Upload" />
    </form>
    {% if upload_message %}
      {% if file_readable %}
        <pre tabindex="0" aria-live="polite">{{ upload_message }}</pre>
      {% else %}
        <div class="message" role="alert">{{ upload_message }}</div>
      {% endif %}
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    upload_message = None
    file_readable = False
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    upload_message = f.read()
                file_readable = True
            except Exception:
                upload_message = "The file uploaded is not a readable text file or is corrupted."
        else:
            upload_message = "No file selected."

    return render_template_string(HTML_TEMPLATE, upload_message=upload_message, file_readable=file_readable)

if __name__ == '__main__':
    app.run(debug=True)

