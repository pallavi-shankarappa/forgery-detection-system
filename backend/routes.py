from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.image_processor import detect_forgery
from models import ScanResult, db

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Unique name to avoid collisions
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        try:
            # Run forgery detection
            result = detect_forgery(file_path)
            
            # Save to database
            scan = ScanResult(
                original_filename=filename,
                stored_filename=unique_filename,
                ela_filename=result['ela_image'],
                is_forged=result['is_forged'],
                confidence_score=result['confidence_score'],
                metadata_markers=",".join(result['metadata_markers']),
                analysis_summary=result['analysis_summary']
            )
            db.session.add(scan)
            db.session.commit()
            
            # Prepare response
            return jsonify({
                "id": scan.id,
                "filename": filename,
                "is_forged": result['is_forged'],
                "confidence_score": result['confidence_score'],
                "ela_url": url_for('api.get_uploaded_file', filename=result['ela_image'], _external=True),
                "original_url": url_for('api.get_uploaded_file', filename=unique_filename, _external=True),
                "analysis_summary": result['analysis_summary'],
                "timestamp": scan.created_at.isoformat()
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"error": "Invalid file type"}), 400

@api_bp.route('/files/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@api_bp.route('/history', methods=['GET'])
def get_history():
    scans = ScanResult.query.order_by(ScanResult.created_at.desc()).limit(10).all()
    results = []
    for scan in scans:
        results.append({
            "id": scan.id,
            "filename": scan.original_filename,
            "is_forged": scan.is_forged,
            "confidence_score": scan.confidence_score,
            "timestamp": scan.created_at.isoformat()
        })
    return jsonify(results)

@api_bp.route('/report/<int:scan_id>', methods=['GET'])
def get_report(scan_id):
    scan = ScanResult.query.get_or_404(scan_id)
    # Placeholder for PDF generation
    return jsonify({
        "id": scan.id,
        "message": "Report generation logic will be added here"
    })
