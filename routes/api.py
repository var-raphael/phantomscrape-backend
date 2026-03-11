from flask import Blueprint, jsonify, request
from modules import scrape_page, clean_data, export_data, insert_job, insert_result, fetch_jobs, fetch_results, update_result_status
from modules.database import supabase

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@api.route("/scrape/bulk", methods=["POST"])
def scrape_bulk():
    data = request.get_json()

    if not data or "urls" not in data:
        return jsonify({"error": "urls array is required"}), 400

    urls = data["urls"]
    throttle = data.get("throttle", 3)
    format = data.get("format", "json")

    if not isinstance(urls, list) or len(urls) == 0:
        return jsonify({"error": "urls must be a non-empty array"}), 400

    job_id = insert_job(urls, throttle, format)

    # Pre-insert all URLs as queued
    result_ids = []
    for url in urls:
        result_id = insert_result(job_id, url, None, [], None, False, "queued")
        result_ids.append((url, result_id))

    results = []

    for url, result_id in result_ids:
        try:
            update_result_status(result_id, "scraping")

            raw = scrape_page(url, throttle=throttle)
            cleaned = clean_data(raw["text"])

            result = {
                "url": url,
                "title": raw["title"],
                "links": raw["links"],
                "cleaned": cleaned
            }

            exported = export_data(result, format)

            supabase.table("results").update({
                "title": raw["title"],
                "links": raw["links"],
                "cleaned": cleaned,
                "success": True,
                "status": "completed"
            }).eq("id", result_id).execute()

            results.append({"url": url, "success": True, "data": exported})

        except Exception as e:
            update_result_status(result_id, "failed")
            results.append({"url": url, "success": False, "error": str(e)})

    supabase.table("jobs").update({"status": "completed"}).eq("id", job_id).execute()

    return jsonify({"success": True, "job_id": job_id, "format": format, "results": results})

@api.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = fetch_jobs()
    return jsonify({"jobs": jobs})

@api.route("/jobs/<job_id>", methods=["GET"])
def get_job_results(job_id):
    results = fetch_results(job_id)
    return jsonify({"results": results})