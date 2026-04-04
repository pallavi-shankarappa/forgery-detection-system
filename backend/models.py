from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    ela_filename = db.Column(db.String(255), nullable=True)
    is_forged = db.Column(db.Boolean, default=False)
    confidence_score = db.Column(db.Float, default=0.0)
    metadata_markers = db.Column(db.Text, nullable=True)
    analysis_summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ScanResult {self.original_filename} - Forged: {self.is_forged}>'
