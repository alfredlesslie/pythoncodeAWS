import os
from flask import Flask, render_template, request
import boto3
import pymysql

app = Flask(__name__)

BUCKET_NAME = "alfred-student-photos-2026"

def get_db_connection():
    return pymysql.connect(
        host="database-1.czi2guu0kb6p.eu-north-1.rds.amazonaws.com",
        port=3306,
        user="admin",
        password=os.environ["DB_PASSWORD"],
        database="pythonapp",
        connect_timeout=10
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    photo = request.files["photo"]

    s3 = boto3.client("s3")

    s3.upload_fileobj(
        photo,
        BUCKET_NAME,
        photo.filename
    )

    photo_url = (
        f"https://{BUCKET_NAME}.s3.amazonaws.com/"
        f"{photo.filename}"
    )

    db = get_db_connection()

    try:
        with db.cursor() as cursor:
            sql = """
                INSERT INTO students
                (name, email, course, photo_url)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (name, email, course, photo_url)
            )

        db.commit()
    finally:
        db.close()

    return "Student Registered Successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
