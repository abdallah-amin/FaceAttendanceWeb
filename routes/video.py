from flask import Blueprint, Response
from camera.worker import CameraWorker

video_bp = Blueprint("video", __name__)

camera: CameraWorker = None

@video_bp.route("/video_feed")
def video_feed():
    def gen():
        while True:
            frame = camera.get_jpeg()
            if frame is None:
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame +
                b"\r\n"
            )

    return Response(
        gen(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )
