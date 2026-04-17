# RoadCare - AI-Based Road Damage & Pothole Detection System

RoadCare is a full-stack pothole reporting and road-risk management system. Citizens submit road images and GPS coordinates through a React frontend, the FastAPI backend verifies the submission, MongoDB stores reports and audit data, and an H3-based geospatial layer groups verified potholes into risk zones for authority review.

## Core Capabilities

- Citizen login, signup, and authenticated pothole reporting
- Browser-based image upload with automatic geolocation capture
- AI-assisted verification using OpenCV-based image analysis
- Authority dashboard for triage, review, and repair workflow tracking
- H3 hexagonal clustering for risk-zone creation
- Role-based access control for citizen and authority users
- MongoDB-backed persistence with indexes for reports, zones, and repairs

## Architecture

User -> React UI -> FastAPI API -> Image Verification -> MongoDB -> H3 Clustering -> Authority Dashboard

### Why this architecture

- The frontend handles presentation and user interaction.
- The API owns authentication, file upload, validation, and business rules.
- MongoDB stores flexible document-shaped data such as reports, verification results, and risk zones.
- H3 gives stable spatial bucketing without square-grid bias.
- The current verification engine is lightweight and explainable, which makes it practical for a project-scale system and easier to defend academically.

## Technology Stack

- Frontend: React, Vite, Axios, React Router
- Backend: Python, FastAPI, Uvicorn, Motor
- Computer Vision: OpenCV, NumPy, Pillow
- Database: MongoDB
- Geospatial: Uber H3
- Testing: pytest, API and integration test suites, frontend E2E tests

## Project Structure

- `backend/app/main.py` - FastAPI application entry point
- `backend/app/routes/` - auth, report, zone, and repair endpoints
- `backend/app/services/` - image verification and clustering logic
- `backend/app/config/database.py` - MongoDB connection and index creation
- `frontend1/src/` - React application, pages, components, and API client

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB running locally or reachable through a connection string

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Frontend

```bash
cd frontend1
npm install
npm run dev
```

## Environment Variables

The backend expects a `.env` file with at least:

- `JWT_SECRET_KEY`
- `MONGODB_URI`
- `MONGODB_DB_NAME`

Optional values exist for test credentials and upload configuration.

## Main Workflows

### Citizen flow

1. Register or log in.
2. Upload a pothole image.
3. Allow browser geolocation, or use the fallback coordinates.
4. Submit the report.
5. Review the AI verification status on the returned result.

### Authority flow

1. Log in with authority credentials.
2. Review submitted reports.
3. Inspect confidence scores, locations, and report status.
4. View clustered risk zones.
5. Create or update repair actions.

## Technical Notes

- Reports are stored with their H3 cell index so spatial grouping is repeatable.
- Verification history is stored separately from the report record to preserve auditability.
- Passwords are hashed before storage and protected endpoints require JWT bearer authentication.
- The current verification path is heuristic rather than a large trained deep model, so it is easier to explain and operate but less robust than a fully trained detector under extreme conditions.

## Testing

The repository includes backend unit, integration, geospatial, and database tests, plus frontend end-to-end coverage. The most recent validation pass showed the critical auth, reporting, and dashboard flows working after stale test expectations were corrected.

## Limitations

- Low light, blur, shadows, and road patches can reduce verification accuracy.
- Risk-zone recalculation currently rebuilds clustered zones from verified reports, so concurrent reads may briefly observe a replacement window.
- The system is best suited to pilot or municipal-scale deployments, not yet a national-scale real-time roadway intelligence platform.

## Future Improvements

- Replace the heuristic verifier with a trained CNN or transfer-learned detector
- Add real-time camera or mobile capture workflows
- Introduce transactional or versioned risk-zone rebuilds
- Add stronger object storage and queue-based inference for higher scale

## License

See [LICENSE](LICENSE) for terms.

---

### Step 1 — Download `yolov8x.pt`

Choose **one** of the methods below:

#### ✅ Method A — Auto-download via Python (Easiest)
When you first run `YOLO("yolov8x.pt")`, Ultralytics automatically downloads the model from the internet and saves it locally:
```python
from ultralytics import YOLO
model = YOLO("yolov8x.pt")   # Downloads ~130 MB on first run
```

#### ✅ Method B — Download via pip / CLI
```bash
# Install ultralytics first (if not already)
pip install ultralytics

# Then use the yolo CLI to pull the model weights
yolo export model=yolov8x.pt format=pt   # Downloads yolov8x.pt to current directory
```

### Step 2 — Place the Model File in the Project Root

After downloading, move/copy `yolov8x.pt` to the **project root** directory:

```
AI-Based-Road-Damage-Pothole-Detection-System-main/
├── yolov8x.pt          ← place it here
├── backend/
└── frontend1/
```

**On Windows (PowerShell):**
```powershell
# If downloaded to Downloads folder:
Copy-Item "$env:USERPROFILE\Downloads\yolov8x.pt" -Destination "C:\Users\Admin\React\AI-Based-Road-Damage-Pothole-Detection-System-main\"
```

---

### Step 3 — Install the `ultralytics` Dependency

Make sure the Ultralytics package is installed in your Python environment:

```bash
cd backend
pip install ultralytics
# or install all dependencies at once:
pip install -r requirements.txt
```

Verify it works:
```bash
python -c "from ultralytics import YOLO; print('ultralytics OK')"
```

---

### Step 4 — Configure `.env` to Point to the Model

Open `backend/.env` and add / update these keys:

```env
# Path to yolov8x.pt relative to the backend folder
# Use ../ to go up one level to the project root
YOLO_MODEL_PATH=../yolov8x.pt

# Minimum AI confidence to flag a detection (0.0 to 1.0)
CONFIDENCE_THRESHOLD=0.50
```

---

### Step 5 — Enable YOLOv8 in the AI Verification Service

Open `backend/app/services/ai_verification_service.py` and replace the `__init__` and `verify_pothole` methods with the YOLOv8-powered version:

```python
import os
from ultralytics import YOLO

class AIVerificationService:
    def __init__(self):
        self.min_confidence = float(os.getenv("CONFIDENCE_THRESHOLD", 0.50)) * 100
        self.auto_verify_threshold = 75.0

        model_path = os.getenv("YOLO_MODEL_PATH", "../yolov8x.pt")
        if os.path.exists(model_path):
            self.yolo = YOLO(model_path)
            print(f"✅ YOLOv8 model loaded from: {model_path}")
        else:
            # Auto-download from Ultralytics if not found locally
            print("⚠️  yolov8x.pt not found locally — downloading automatically...")
            self.yolo = YOLO("yolov8x.pt")  # Triggers auto-download

    async def verify_pothole(self, image_path: str, report_id) -> VerificationInDB:
        if self.yolo:
            results = self.yolo(image_path, conf=self.min_confidence / 100)[0]
            scores = [float(b.conf[0]) * 100 for b in results.boxes] if results.boxes else []
            confidence_score = max(scores, default=0.0)
            is_pothole = confidence_score >= self.min_confidence
        else:
            confidence_score, is_pothole = await self._analyze_image(image_path)
            confidence_score = min(confidence_score * 1.15, 100.0)

        return VerificationInDB(
            report_id=report_id,
            is_pothole=is_pothole,
            confidence_score=round(confidence_score, 2),
            verified_at=datetime.utcnow()
        )
```

---

### Step 6 — Test the Integration

1. **Start the backend:**
   ```bash
   cd backend
   python run.py
   ```
   You should see in the logs:
   ```
   ✅ YOLOv8 model loaded from: ../yolov8x.pt
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

2. **Submit a test image** via the citizen portal at `http://localhost:3000`
   → Upload a road/pothole photo → Check the authority dashboard for AI confidence score.

3. **Quick standalone Python test:**
   ```python
   from ultralytics import YOLO
   model = YOLO("yolov8x.pt")
   results = model("path/to/road_image.jpg")
   results[0].show()        # Opens window with bounding boxes
   results[0].save()        # Saves annotated image to runs/detect/
   print(results[0].boxes)  # Prints detection details
   ```

---

### YOLOv8 Model Variants Comparison

| Model | File Size | Speed | Accuracy | Best For |
|-------|-----------|-------|----------|----------|
| `yolov8n.pt` | 6 MB | ⚡ Fastest | Lowest | Low-end / Edge devices |
| `yolov8s.pt` | 22 MB | Fast | Moderate | Development / Testing |
| `yolov8m.pt` | 50 MB | Balanced | Good | Production (CPU) |
| **`yolov8x.pt`** | **130 MB** | Moderate | **Highest ✅** | **Best accuracy — Recommended** |

> 💡 `yolov8x.pt` uses ~1–2 GB RAM during inference. A CUDA-enabled NVIDIA GPU will give **3–5× faster** processing. CPU-only mode still works but is slower.

---

## 📄 License

MIT License

---

## 📘 Repository Architecture & System Documentation

### 1. Project Overview

RoadCare is a production-grade Road Infrastructure Management System designed for municipal governments, road authorities, and civic bodies to efficiently detect, verify, and coordinate repair of road damage. It bridges the gap between passive citizen complaints and proactive damage detection using Computer Vision technology.

Unlike traditional manual inspection processes, RoadCare leverages AI-powered image recognition to automatically identify and classify pavement defects from citizen-submitted photos. The system then facilitates authority verification, repair planning, and progress tracking through an integrated dashboard and notification system.

**Key Technologies:**

- **Computer Vision**: YOLOv8 (Object Detection), OpenCV (Image Processing), Damage Classification Models
- **Backend Architecture**: FastAPI (High-performance Async I/O), WebSockets (Real-time updates)
- **Frontend Interface**: React + Vite (Responsive dashboard, mobile-optimized citizen portal)
- **Infrastructure**: SQLite/PostgreSQL (Data Persistence), RESTful APIs

### 2. Repository Structure & File Responsibilities

```
AI-Based-Road-Damage-Pothole-Detection-System/
│
├── backend/                       # Python Backend & AI Engine
│   ├── app/
│   │   ├── config/                # Database & app configuration
│   │   ├── models/                # SQLAlchemy ORM models
│   │   │   ├── report.py          # Damage report schema
│   │   │   ├── user.py            # User authentication
│   │   │   ├── repair.py          # Repair tracking
│   │   │   ├── verification.py    # AI verification results
│   │   │   └── risk_zone.py       # High-risk area mapping
│   │   ├── routes/                # API endpoints
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── reports.py         # Report management
│   │   │   ├── repairs.py         # Repair coordination
│   │   │   └── zones.py           # Risk zone analysis
│   │   ├── services/              # Business logic & AI
│   │   │   ├── ai_verification_service.py  # MAIN AI ENGINE: Damage classification
│   │   │   ├── image_service.py   # Image processing & storage
│   │   │   └── clustering_service.py # Damage hotspot detection
│   │   ├── utils/
│   │   │   ├── auth.py            # JWT token handling
│   │   │   └── validators.py      # Input validation
│   │   ├── main.py                # Application Entry Point
│   │   └── __init__.py
│   ├── requirements.txt           # Python dependencies
│   ├── requirements-dev.txt       # Development dependencies
│   ├── run.py                     # Server launcher
│   └── uploads/                   # Temporary image storage
│
├── frontend1/                     # React Frontend
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── Toast.jsx
│   │   ├── pages/                 # Application views
│   │   │   ├── HomePage.jsx
│   │   │   ├── ReportPotholePage.jsx    # Citizen report form
│   │   │   ├── CitizenLoginPage.jsx
│   │   │   ├── CitizenSignupPage.jsx
│   │   │   ├── AuthorityLoginPage.jsx
│   │   │   ├── AuthorityDashboardPage.jsx # Admin verification panel
│   │   │   ├── ComplaintDetailPage.jsx
│   │   │   ├── RecentReportsPage.jsx
│   │   │   ├── ContactPage.jsx
│   │   │   └── HowItWorksPage.jsx
│   │   ├── context/               # Global state management
│   │   │   ├── AuthContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── services/              # API integration
│   │   │   └── apiService.js
│   │   ├── utils/
│   │   │   └── storageUtils.js
│   │   ├── config/
│   │   │   └── config.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── setup_project.py               # Automated setup & verification
├── requirements.txt               # Root dependencies (if any)
├── .env                           # Environment configuration (not in git)
├── .gitignore
├── pytest.ini                     # Testing configuration
├── MIGRATION.md                   # Frontend migration notes
└── README.md                      # This file
```

### 3. Environment Variables & Configuration

The system follows 12-Factor App principles with all configuration via `.env` file.

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| **DATABASE_URL** | Connection String | YES | SQLite or PostgreSQL connection (e.g., `sqlite:///./roadcare.db`) |
| **SECRET_KEY** | String | YES | Application secret for encryption |
| **JWT_SECRET** | String | YES | Cryptographic key for JWT tokens |
| **ALGORITHM** | String | No | JWT algorithm (Default: HS256) |
| **ACCESS_TOKEN_EXPIRE_MINUTES** | Integer | No | Token expiration time (Default: 30) |
| **TELEGRAM_BOT_TOKEN** | String | No | Telegram bot token for notifications |
| **TELEGRAM_CHAT_ID** | String | No | Target Telegram chat/channel ID |
| **CONFIDENCE_THRESHOLD** | Float | No | AI confidence minimum for damage detection (Default: 0.60) |
| **YOLO_MODEL_PATH** | Path | No | Path to custom YOLO model |
| **MODEL_CACHE_DIR** | Path | No | Directory for ML model caching |

### 4. Dependency Analysis

**Backend Core:**
- `fastapi`, `uvicorn`: High-performance ASGI web server framework
- `sqlalchemy`: ORM for database operations
- `pydantic`: Data validation and settings management

**Deep Learning & Vision:**
- `ultralytics`: YOLOv8 implementation for damage detection
- `opencv-python`: Image processing (resizing, normalization, encoding)
- `pillow`: Image manipulation and format conversion
- `numpy`: Numerical operations on image arrays

**Infrastructure:**
- `sqlalchemy`: Database ORM for PostgreSQL/SQLite
- `python-telegram-bot`: Async Telegram API wrapper
- `python-jose`, `passlib`: JWT tokens and password hashing
- `python-multipart`: Multipart form handling for image uploads

**Frontend:**
- `react@18`, `react-dom`: UI framework
- `vite`: Next-generation build tool
- `axios`: HTTP client with interceptors
- `react-router-dom`: Client-side routing
- `tailwindcss`: Utility-first CSS framework

### 5. System & Laptop Configuration Requirements

**Minimum Requirements (CPU Processing):**
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS
- **CPU**: Intel Core i5 (8th Gen) / AMD Ryzen 5 or equivalent
- **RAM**: 8 GB (for model inference)
- **Storage**: 4 GB free space (models, dependencies, cache)
- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Node.js**: 16.x or higher

**Recommended Requirements (Faster Processing):**
- **CPU**: Intel Core i7 (10th Gen+) / AMD Ryzen 7
- **RAM**: 16 GB DDR4
- **GPU**: NVIDIA GTX 1060 (6GB) - optional for ~2-3x faster inference
- **CUDA**: 11.8 or 12.1 (if GPU available)

**Windows-Specific Considerations:**
- Long path support may be needed for deep learning libraries
- Run `python setup_project.py` which handles path configuration automatically

### 6. Application Execution Flow

**Initialization Phase:**
1. `run.py` executes and initializes the FastAPI application
2. `.env` variables are loaded and validated
3. Database connection is established to SQLite/PostgreSQL

**AI Model Initialization:**
1. YOLOv8 model is loaded into memory (auto-downloads if missing)
2. Image processing pipeline is initialized
3. Damage classification model is prepared

**Request Processing Flow:**
1. **Citizen Report**: User uploads image + location data via `/api/reports/create`
2. **Image Ingestion**: Image is stored and normalized
3. **AI Processing**: 
   - YOLOv8 detects damage regions (potholes, cracks)
   - Severity classification determines damage level (Low/Medium/High/Critical)
   - Confidence score > CONFIDENCE_THRESHOLD triggers verification
4. **Authority Verification**: Dashboard displays unverified reports for manual review
5. **Notification**: Telegram alert sent to authorities for high-severity cases
6. **Tracking**: Repair status updated as crews work on fixes

### 7. Setup & Installation Best Practices

1. **Virtual Environment**: Use `python -m venv venv` to isolate dependencies
2. **Dependencies**: Run `pip install -r requirements.txt` after activation
3. **Database**: Initialize with `python setup_project.py` or manual migration
4. **Frontend**: Install Node modules with `npm install` in `frontend1/`
5. **Configuration**: Always create `.env` with sensitive keys before running

### 8. Security & Best Practices

- **Secret Management**: Never commit `.env` to version control
- **Authentication**: JWT tokens required for authority dashboard access
- **Input Validation**: All user inputs validated via Pydantic schemas
- **Image Security**: Uploaded images scanned before processing
- **Rate Limiting**: API endpoints implement request throttling (60 req/min)
- **CORS**: Cross-origin requests restricted to authorized domains
- **HTTPS**: Enable in production via reverse proxy (Nginx/Apache)

---

📄 Documentation auto-generated by repository analysis. All project-specific details adapted to RoadCare infrastructure management system.
