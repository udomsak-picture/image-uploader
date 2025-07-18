from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    links = []
    if request.method == "POST":
        files = request.files.getlist("file")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                links.append(url_for("uploaded_file", filename=filename))
    return render_template("index.html", links=links)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return f"https://drive.google.com/uc?export=view&id={filename}"

if __name__ == "__main__":
    app.run(debug=True)
