from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXETENSIONS = {'webp', 'gif', 'jpg', 'png', 'jpeg'}

app = Flask(__name__)
app.secret_key = "my secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXETENSIONS


def Processimg(filename, operation):
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgary":
            imgp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgp)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    operation = request.form.get("operation")
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file Part')
            return "error"
        file = request.files['file']
        if file.filename == '':
            flash("No file Selected")
            return "Error No Selected File."
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = Processimg(filename, operation)
            flash(
                f"Your Image hans been processed watch it out <a href='/{new}' target='_blank'>here</a>")
            return render_template('index.html')


app.run(debug=True)
