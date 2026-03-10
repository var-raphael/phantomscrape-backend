import json
import csv
import io
import xml.etree.ElementTree as ET

def export_json(data: dict) -> str:
    return json.dumps(data, indent=2)

def export_csv(data: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(data.keys())
    writer.writerow(data.values())
    return output.getvalue()

def export_xml(data: dict) -> str:
    root = ET.Element("result")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    return ET.tostring(root, encoding="unicode")

def export_txt(data: dict) -> str:
    lines = [f"{key}: {value}" for key, value in data.items()]
    return "\n".join(lines)

def export_html(data: dict) -> str:
    rows = "".join(f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in data.items())
    return f"<table border='1'>{rows}</table>"

def export_data(data: dict, format: str) -> str:
    format = format.lower()
    if format == "json": return export_json(data)
    if format == "csv": return export_csv(data)
    if format == "xml": return export_xml(data)
    if format == "txt": return export_txt(data)
    if format == "html": return export_html(data)
    return export_json(data)