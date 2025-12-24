from flask import Blueprint, jsonify, request, Response
import cv2
import numpy as np
import csv
from io import StringIO

from attendance.service import compute_status
from recognition.faces import encode_faces, match_face
from database.persons import add_person
from camera.worker import CameraWorker


api_bp = Blueprint("api", __name__)

# يتم حقنه من app.py
camera: CameraWorker = None


# =========================
# Attendance Status
# =========================
@api_bp.route("/status")
def api_status():
    """
    جلب الحضور
    ?date=YYYY-MM-DD (اختياري)
    """
    try:
        date_str = request.args.get("date")
        data = compute_status(date_str)
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# Add person from upload
# =========================
@api_bp.route("/add_person/upload", methods=["POST"])
def api_add_person_upload():
    """
    إضافة شخص جديد من صورة مرفوعة
    Form-Data:
      - name
      - image
    """
    try:
        name = request.form.get("name", "").strip()
        if not name:
            return jsonify({"ok": False, "error": "Name is required"}), 400

        if "image" not in request.files:
            return jsonify({"ok": False, "error": "Image file is required"}), 400

        file = request.files["image"]
        data = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"ok": False, "error": "Invalid image"}), 400

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encs, _ = encode_faces(rgb)

        if not encs:
            return jsonify({"ok": False, "error": "No face detected"}), 400

        encoding = encs[0]

        # هل الشخص موجود؟
        existing, _ = match_face(encoding)
        if existing:
            return jsonify({
                "ok": False,
                "error": f"Person already exists as '{existing['name']}'"
            }), 400

        add_person(name, encoding)

        return jsonify({"ok": True, "msg": "Person added successfully"})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# Add person from camera (Unknown)
# =========================
@api_bp.route("/add_person/from_camera", methods=["POST"])
def api_add_person_from_camera():
    """
    JSON:
      { "name": "Person Name" }
    """
    try:
        name = request.json.get("name", "").strip()
        if not name:
            return jsonify({"ok": False, "error": "Name is required"}), 400

        if camera is None or camera.last_unknown_encoding is None:
            return jsonify({
                "ok": False,
                "error": "No unknown face detected in camera"
            }), 400

        encoding = camera.last_unknown_encoding

        # هل موجود قبل كده؟
        existing, _ = match_face(encoding)
        if existing:
            return jsonify({
                "ok": False,
                "error": f"Person already exists as '{existing['name']}'"
            }), 400

        add_person(name, encoding)

        # نفضي آخر unknown
        camera.last_unknown_encoding = None

        return jsonify({"ok": True, "msg": "Person added successfully"})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# Download attendance CSV
# =========================
@api_bp.route("/attendance/csv")
def api_attendance_csv():
    """
    تحميل الحضور كـ CSV
    ?date=YYYY-MM-DD (اختياري)
    """
    try:
        date_str = request.args.get("date")
        data = compute_status(date_str)

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Name", "Time", "Date"])

        for row in data["present"]:
            writer.writerow([row["name"], row["time"], data["date"]])

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=attendance_{data['date']}.csv"
            }
        )

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
