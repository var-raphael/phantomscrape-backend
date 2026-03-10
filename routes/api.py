from flask import Blueprint, jsonify, request
from modules import scrape_page, clean_data, export_data


api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@api.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "url is required"}), 400

    url = data["url"]
    throttle = data.get("throttle", 3)
    format = data.get("format", "json")

    raw = scrape_page(url, throttle=throttle)

    cleaned = clean_data(raw["text"])

    result = {
        "url": url,
        "title": raw["title"],
        "links": raw["links"],
        "cleaned": cleaned
    }

    exported = export_data(result, format)

    return jsonify({
        "success": True,
        "format": format,
        "data": exported
    })
    
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

    results = []

    for url in urls:
        try:
            raw = scrape_page(url, throttle=throttle)
            cleaned = clean_data(raw["text"])
            result = {
                "url": url,
                "title": raw["title"],
                "links": raw["links"],
                "cleaned": cleaned
            }
            exported = export_data(result, format)
            results.append({"url": url, "success": True, "data": exported})
        except Exception as e:
            results.append({"url": url, "success": False, "error": str(e)})

    return jsonify({"success": True, "format": format, "results": results})