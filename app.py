import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import random

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database setup
def init_db():
    conn = sqlite3.connect("annotations.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS annotations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

# Dataset setup
def create_sample_dataset():
    os.makedirs("static/uploads/sample", exist_ok=True)
    categories = ["Car", "Truck", "Bike"]
    for category in categories:
        for i in range(5):  # Generate 5 images per category
            img = Image.new("RGB", (200, 200), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            text = f"{category} {i+1}"
            text_width, text_height = draw.textsize(text, font=font)
            text_x = (img.width - text_width) // 2
            text_y = (img.height - text_height) // 2
            draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
            filename = f"{category.lower()}_{i+1}.jpg"
            img.save(os.path.join("static/uploads/sample", filename))

# Routes
@app.route('/')
def home():
    conn = sqlite3.connect("annotations.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM annotations")
    data = cursor.fetchall()
    conn.close()
    return render_template("home.html", annotations=data)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for("home"))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for("home"))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    conn = sqlite3.connect("annotations.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO annotations (filename) VALUES (?)", (file.filename,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route('/update_status/<int:annotation_id>', methods=['POST'])
def update_status(annotation_id):
    new_status = request.form.get("status")
    conn = sqlite3.connect("annotations.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE annotations SET status = ? WHERE id = ?", (new_status, annotation_id))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route('/delete/<int:annotation_id>', methods=['POST'])
def delete_annotation(annotation_id):
    conn = sqlite3.connect("annotations.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM annotations WHERE id = ?", (annotation_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

if __name__ == '__main__':
    init_db()
    create_sample_dataset()
    app.run(debug=True)
