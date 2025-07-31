import psycopg2

# Replace with your Supabase credentials
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    sslmode="require"
)


def load_jobs_from_db():
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, location, salary FROM jobs;")
    jobs = []
    for row in cursor.fetchall():
        jobs.append({
            'id': row[0],
            'title': row[1],
            'location': row[2],
            'salary': row[3]
        })
    cursor.close()
    return jobs

def load_job_from_db(job_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, location, salary FROM jobs WHERE id = %s", (job_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return {
            'id': row[0],
            'title': row[1],
            'location': row[2],
            'salary': row[3]
        }
    else:
        return None
