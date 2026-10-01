# RoadCare – AI-Based Road Damage & Pothole Detection System

## 📌 Overview

RoadCare is an AI-powered web application designed to help citizens report potholes and road damage and help authorities manage, verify, and track reported road issues.

The system combines image-based AI verification with location information to provide a structured platform for reporting and managing road damage.

## 🎯 Problem Statement

Potholes and damaged roads can create serious safety risks for commuters. Traditional reporting methods can be slow and may not provide enough information for authorities to verify and prioritize road-damage complaints.

RoadCare provides a centralized platform where citizens can submit pothole reports along with images and location details, while authorities can review and manage these reports.

## 💡 Proposed Solution

RoadCare allows users to:

- Upload images of potholes or road damage.
- Provide the location of the reported issue.
- Add a description of the road damage.
- Receive AI-based image verification.
- Track the status of submitted reports.

Authorities can:

- View submitted reports.
- Review pothole images and locations.
- Verify or reject reports.
- Update the status of reports.
- Manage the repair workflow.

## ✨ Key Features

### 👤 Citizen Module

- User registration and login
- Submit pothole reports
- Upload pothole images
- Provide GPS location
- Add report descriptions
- View submitted reports
- Track report status

### 🏛️ Authority Module

- Authority authentication
- View reported potholes
- Review submitted complaints
- View uploaded images
- Verify or reject reports
- Update report status
- Manage repair-related status updates

### 🤖 AI Verification

- Image-based pothole verification
- AI confidence score
- Automatic verification/rejection based on AI results
- YOLO-based pothole detection

### 📍 Location-Based Reporting

Each report contains:

- Latitude
- Longitude
- Location information
- H3 location index

This helps organize reported road-damage locations geographically.

## 🛠️ Technology Stack

### Frontend

- React
- JavaScript
- Vite
- HTML
- CSS

### Backend

- Python
- FastAPI
- REST APIs

### AI / Computer Vision

- YOLO
- OpenCV
- Python

### Database

- MongoDB

### Development Tools

- Git
- GitHub
- VS Code

## 🔄 System Workflow

```text
Citizen
   ↓
Login / Registration
   ↓
Upload Pothole Image
   ↓
Provide Location & Description
   ↓
AI Verification
   ↓
Report Stored in Database
   ↓
Authority Reviews Report
   ↓
Verify / Reject
   ↓
Update Repair Status
   ↓
Citizen Tracks Report
```
## 📂 Project Structure

```text
RoadCare-AI-Pothole-Detection-System/
│
├── backend/
│   ├── app/
│   │   ├── config/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── ...
│
├── frontend1/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── yolo_dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── data.yaml
│
├── test_images/
│
├── README.md
└── LICENSE
```



## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/chinmayee1701/RoadCare-AI-Pothole-Detection-System.git
cd RoadCare-AI-Pothole-Detection-System
```

### 2. Backend Setup

Open PowerShell or Command Prompt:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend1
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

## 🤖 AI Model

RoadCare uses a YOLO-based object detection approach for pothole detection and image verification.

The AI verification workflow analyzes uploaded road images and provides a confidence score that is used as part of the report verification process.

### AI Workflow

```text
Uploaded Image
      ↓
Image Processing
      ↓
YOLO-Based Detection
      ↓
Pothole Verification
      ↓
Confidence Score
      ↓
Report Status Update
```

## 👩‍💻 My Role

### Team Lead — Lakshmi Sai Chinmayee Kalangi

As the Team Lead, I coordinated the development of the project and contributed to its technical implementation.

- Led and coordinated the project team.
- Coordinated project development and task distribution.
- Contributed to the AI/ML-based pothole detection workflow.
- Worked on backend API development and report management.
- Contributed to frontend and backend integration.
- Implemented and tested report status and repair workflows.
- Worked on debugging and resolving application issues.
- Coordinated project documentation and final integration.

  ## 🔮 Future Enhancements

- Real-time pothole detection using mobile cameras
- Improved road-damage classification
- Enhanced map-based visualization
- Automated repair-priority recommendations
- Mobile application support
- Expansion of the training dataset
- Improved AI model performance

  ## 📄 License

This project is licensed under the Apache License 2.0.

