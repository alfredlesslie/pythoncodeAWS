import os

import boto3
import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)

# S3 configuration
bucket_name = "alfred-student-photos-2026"
s3 = boto3.client("s3")


def get_db_connection():
    """Create a connection to the RDS MySQL database."""
    return pymysql.connect(
        host="database-1.czi2guu0kb6p.eu-north-1.rds.amazonaws.com",
        port=int(3306),
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

    photo = request.files.get("photo")
    photo_url = None

    # Upload the photo to S3 if one was provided
    if photo and photo.filename:
        s3.upload_fileobj(
            photo,
            bucket_name,
            photo.filename
        )
        photo_url = (
            f"https://{bucket_name}.s3.amazonaws.com/{photo.filename}"
        )

    # Save student details to RDS
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO students
                    (name, email, course, photo_url)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (name, email, course, photo_url)
            )

        connection.commit()

    finally:
        connection.close()

    return "Student registered successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
