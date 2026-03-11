import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def insert_job(urls: list, throttle: int, format: str) -> str:
    res = supabase.table("jobs").insert({
        "urls": urls,
        "throttle": throttle,
        "format": format,
        "status": "completed"
    }).execute()
    print("INSERT JOB RESPONSE:", res)
    return res.data[0]["id"]

def insert_result(job_id: str, url: str, title: str, links: list, cleaned: str, success: bool):
    supabase.table("results").insert({
        "job_id": job_id,
        "url": url,
        "title": title,
        "links": links,
        "cleaned": cleaned,
        "success": success
    }).execute()

def fetch_jobs():
    res = supabase.table("jobs").select("*").order("created_at", desc=True).execute()
    return res.data

def fetch_results(job_id: str):
    res = supabase.table("results").select("*").eq("job_id", job_id).execute()
    return res.data
    
def update_result_status(result_id: str, status: str):
    supabase.table("results").update(
        {"status": status}
    ).eq("id", result_id).execute()
    
def insert_result(job_id: str, url: str, title: str, links: list, cleaned: str, success: bool, status: str = "queued"):
    res = supabase.table("results").insert({
        "job_id": job_id,
        "url": url,
        "title": title,
        "links": links,
        "cleaned": cleaned,
        "success": success,
        "status": status
    }).execute()
    return res.data[0]["id"]