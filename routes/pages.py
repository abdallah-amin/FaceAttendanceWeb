from flask import Blueprint, render_template

from camera.worker import CameraWorker

pages_bp = Blueprint("pages", __name__)

# يتم حقنه من app.py
camera: CameraWorker = None


@pages_bp.route("/")
def home():
    # تصفير الذاكرة المؤقتة فقط (مش الداتابيز)
    if camera is not None:
        camera.seen_today = set()

    return render_template("index.html")


@pages_bp.route("/attendance")
def attendance_page():
    """
    صفحة جدول الحضور + البحث بالتاريخ + تحميل CSV
    """
    return render_template("attendance.html")
