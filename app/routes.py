from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import re
import json

from app.analyzer import analyzer

routes = Blueprint('routes', __name__)


@routes.route('/analyze', methods=['POST'])
def analyze_file():
    if "file" not in request.files:
        return jsonify({"status": "FAILED", "message": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "" or not analyzer.allowed_file(file.filename):
        return jsonify({"status": "FAILED", "message": "Invalid file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = f"{analyzer.upload_folder}/{filename}"
    file.save(file_path)
    
    # extract text
    if filename.endswith('.pdf'):
        text = analyzer.extract_text_from_pdf(file_path)
    elif filename.endswith('.docx'):
        text = analyzer.extract_text_from_docx(file_path)
    else:
        return jsonify({"status": "FAILED", "message": "Unsupported file type"}), 400
    
    # analyze text
    analysis_result = analyzer.analyze_text(text)
    if "error" in analysis_result:
        return jsonify({"status": "FAILED", "message": analysis_result["error"], "details": analysis_result.get("details")}), 500
    
    # return jsonify({"status": "SUCCESS", "data": analysis_result}), 200
    model_text = analysis_result["response"]
    try:
        json_str = re.search(r"\{[\s\S]*\}", model_text).group()
        data = {"analysis": json.loads(json_str), "raw": False}
        return jsonify({"status": "SUCCESS", "data": data}), 200
    except Exception as e:
        print(f"Error parsing JSON from model response: {e}")
        data = {"analysis": model_text, "raw": True}
        return jsonify({"status": "SUCCESS", "data": data}), 200
    