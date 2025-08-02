from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
from supabase import create_client, Client
from database import load_jobs_from_db, load_job_from_db
import psycopg2

# Load Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Supabase credentials missing. Please check .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Optional PostgreSQL connection check
try:
    if all([
        os.getenv("DB_NAME"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT")
    ]):
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("✅ Connected to Supabase PostgreSQL")
    else:
        print("⚠️ PostgreSQL environment variables missing. Skipping DB connection.")
except Exception as e:
    print("❌ DB connection error:", e)

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        # Save job to database here
        # title = request.form['title']
        # location = request.form['location']
        # salary = request.form['salary']
        # ...save to DB...
        return render_template('post_job.html', submitted=True)
    return render_template('post_job.html', submitted=False)

@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route("/apply/<int:job_id>", methods=['GET', 'POST'])
def apply(job_id):
    job = load_job_from_db(job_id)
    if not job:
        return "Job not found", 404

    if request.method == 'POST':
        name = request.form.get("fullname")
        email = request.form.get("email")
        skills = request.form.get("skills")
        location = request.form.get("location")
        coverletter = request.form.get("coverletter")

        photo_file = request.files.get("photo")
        resume_file = request.files.get("resume")

        resume_url = None
        photo_url = None

        # Upload resume to Supabase Storage (user-uploads/resumes)
        if resume_file:
            try:
                resume_bytes = resume_file.read()
                resume_filename = f"resumes/{datetime.utcnow().isoformat()}_{resume_file.filename}"
                supabase.storage.from_("user-uploads").upload(
                    path=resume_filename,
                    file=resume_bytes,
                    file_options={"content-type": resume_file.content_type}
                )
                resume_url = supabase.storage.from_("user-uploads").get_public_url(resume_filename)
            except Exception as e:
                print("❌ Resume upload failed:", e)

        # Upload photo to Supabase Storage (user-uploads/photos)
        if photo_file:
            try:
                photo_bytes = photo_file.read()
                photo_filename = f"photos/{datetime.utcnow().isoformat()}_{photo_file.filename}"
                supabase.storage.from_("user-uploads").upload(
                    path=photo_filename,
                    file=photo_bytes,
                    file_options={"content-type": photo_file.content_type}
                )
                photo_url = supabase.storage.from_("user-uploads").get_public_url(photo_filename)
            except Exception as e:
                print("❌ Photo upload failed:", e)

        # Insert data into Supabase table
        try:
            response = supabase.table("applications").insert({
                "job_id": job_id,
                "name": name,
                "email": email,
                "skills": skills,
                "location": location,
                "coverletter": coverletter,
                "resume": resume_url,
                "photo": photo_url
            }).execute()
            print("✅ Application saved:", response.data)
        except Exception as e:
            print("❌ Error saving application:", e)
            return "Something went wrong while submitting the application", 500

        return render_template("apply.html", submitted=True, job=job)

    return render_template("apply.html", job=job)


@app.route("/requirements/<int:job_id>")
def requirements(job_id):
    job = load_job_from_db(job_id)
    if not job:
        return "Job not found", 404
    return render_template("requirement.html", job=job)

@app.route('/home')
def home():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
