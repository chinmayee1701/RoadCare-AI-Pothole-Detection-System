# RoadCare - AI-Based Road Damage & Pothole Detection System

RoadCare is an advanced autonomous road infrastructure monitoring system leveraging Deep Learning (YOLOv8, Image Classification) to detect road damage, potholes, and other pavement defects in real-time. It provides instant citizen reporting via mobile apps, AI verification by authorities, and automated repair coordination through Telegram notifications and a centralized dashboard.

## 🚀 Features

- **Real-Time Damage Detection**: Detects potholes, cracks, and road damage using custom-trained YOLOv8 models
- **Citizen Reporting**: Mobile-friendly interface for citizens to report damage with photos and GPS location
- **AI Verification**: Automatic damage classification and severity assessment using deep learning models
- **Authority Dashboard**: Secure management portal for reviewing, verifying, and tracking repair status
- **Smart Notifications**: Real-time alerts via Telegram and dashboard updates for report changes
- **Location-Based Analytics**: Geospatial visualization of damage hotspots and repair progress
- **Secure & Scalable**: Built with FastAPI, React, and MongoDB for production-grade reliability

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, Axios
- **Backend**: Python, FastAPI, Uvicorn, SQLAlchemy
- **Deep Learning**: YOLOv8 (Ultralytics), TensorFlow, PyTorch, OpenCV
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Notifications**: Telegram Bot API
- **APIs**: RESTful architecture with automatic Swagger documentation

## 📦 Installation

### Clone the repository:

```bash
git clone https://github.com/CodeArunJ/AI-Based-Road-Damage-Pothole-Detection-System.git
cd AI-Based-Road-Damage-Pothole-Detection-System
```

### Environment Setup

Create a `.env` file in the root directory with required configuration.

**Required keys:**
- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET`
- `TELEGRAM_BOT_TOKEN` (optional, for notifications)

### Run Verification & Setup

Execute the setup script to validate your environment and install dependencies:

```bash
python setup_project.py
```

### Start the Application

**Backend:**
```bash
cd backend
python run.py
```

**Frontend:**
```bash
cd frontend1
npm install
npm run dev
```

## 🛡️ Usage

1. Access the citizen portal at `http://localhost:3000`
2. Citizens can report potholes with photos and location data
3. Authorities access `http://localhost:3000/authority-login` to verify and manage reports
4. Real-time updates appear in the dashboard
5. Repair coordinators receive Telegram alerts for high-priority damage

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
├── vercel.json                    # Frontend deployment config
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
