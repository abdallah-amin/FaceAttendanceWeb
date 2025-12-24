# Face Attendance Web

A simple web-based face recognition attendance system built with Python and Flask.

The application uses a live camera feed to recognize faces in real time and record attendance without storing any images.

---

## Features

- Live camera streaming on the web
- Real-time face recognition
- Add new persons:
  - From an uploaded image
  - Directly from the camera (unknown face)
- View attendance records
- Search attendance by date
- Export attendance as CSV
- No image storage (only face encodings are saved)
- Optimized camera processing to reduce lag

---

## Technologies

- Python
- Flask
- OpenCV
- face_recognition
- SQLite
- HTML / CSS / JavaScript

---

## How to Run

1. Clone the repository
```bash
git clone https://github.com/USERNAME/FaceAttendanceWeb.git
cd FaceAttendanceWeb
```

2.Install dependencies
  pip install -r requirements.txt

3. Run the application
   python app.py

4. Open your browser at:
  http://127.0.0.1:5000

Author : Abdallah Amin
