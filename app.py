from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

JOBS = [
    {
        'id': 1,
        'title': 'Data Analyst',
        'location': 'Bengaluru, India',
        'salary': 'Rs. 10,00,000'
        
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'Delhi, India',
        'salary': 'Rs. 15,00,000'
      
    },
    {
        'id': 3,
        'title': 'Frontend Engineer',
        'location': 'Remote',
        'salary': 'Rs. 12,00,000'
    },
    {
        'id': 4,
        'title': 'Backend Engineer',
        'location': 'San Francisco, USA',
        'salary': '$120,000'
    },
]

# Homepage
@app.route("/")
def home():
    return render_template("home.html", jobs=JOBS, company_name='Jovian')

# API for jobs
@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

# Application form route with job ID
@app.route("/apply/<int:job_id>")
def apply(job_id):
    job = next((job for job in JOBS if job["id"] == job_id), None)
    if not job:
        return "Job not found", 404
    return render_template("apply.html", job=job, submitted=False)

# Form submission handler
@app.route("/submit/<int:job_id>", methods=["POST"])
def submit_application(job_id):
    job = next((job for job in JOBS if job["id"] == job_id), None)
    if not job:
        return "Job not found", 404

    full_name = request.form.get("fullname")
    email = request.form.get("email")
    skills = request.form.get("skills")
    location = request.form.get("location")

    print("Application Received:", full_name, email, skills, location, f"Job ID: {job_id}")

    return render_template("apply.html", submitted=True, job=job)

@app.route("/requirements/<int:job_id>")
def requirements(job_id):
    job = next((job for job in JOBS if job["id"] == job_id), None)
    if not job:
        return "Job not found", 404
    return render_template("requirement.html", job=job)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
