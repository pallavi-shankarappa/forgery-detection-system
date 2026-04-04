# Forgery Detector Pro 🛡️

Advanced Image Authentication & Digital Forensic Analysis Tool

## 🚀 Overview
Forgery Detector Pro is a professional-grade web application designed to identify digital manipulations in images. Using forensic techniques like **Error Level Analysis (ELA)** and metadata inspection, the tool helps security analysts, journalists, and forensic experts verify the authenticity of digital media.

## ✨ Key Features
- **Advanced Forensic Analysis**: Implements ELA to highlight areas with different compression levels.
- **Metadata Inspection**: Scans for manipulation markers from software like Adobe Photoshop or GIMP.
- **Real-time Dashboard**: Interactive UI for comparing original images with forensic highlights.
- **Historical Tracking**: Stores previous scans in a local database for future reference.
- **Responsive Design**: Modern, mobile-friendly interface with dark/light themes.
- **Recruiter-Ready**: Clean architecture, production-style code, and professional UI.

## 🛠️ Tech Stack
- **Backend**: Python, Flask, SQLAlchemy
- **Forensics**: OpenCV, Pillow (PIL), NumPy
- **Frontend**: Bootstrap 5, FontAwesome, Vanilla JS
- **Database**: SQLite

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/forgery-detector-pro.git
cd forgery-detector-pro
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python -m backend.app
```
The app will be available at `http://localhost:5000`.

## 📁 Project Architecture
```
/
├── backend/            # Flask server, routes, and models
├── frontend/           # (Placeholder for SPA if needed)
├── static/             # Assets (CSS, JS, Images)
├── templates/          # HTML templates (JinJa2)
├── utils/              # Forensic processing logic (ELA, Metadata)
├── uploads/            # Temporary storage for analysis
├── reports/            # Generated PDF reports
├── models/             # ML model weights (if any)
└── requirements.txt    # Project dependencies
```

## 🚀 Deployment
### Deploy to Render
1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. Use the following settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`

## 💡 Future Enhancements
- [ ] Integration with Deep Learning models (CNNs) for localized forgery detection.
- [ ] Support for video forgery (Deepfake) analysis.
- [ ] Cloud storage integration for long-term data persistence.
- [ ] Multi-user authentication and team collaboration features.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
