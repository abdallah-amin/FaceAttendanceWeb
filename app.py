from flask import Flask

from config import CAMERA_INDEX
from camera.worker import CameraWorker

from routes.pages import pages_bp
from routes.api import api_bp
from routes.video import video_bp

import routes.pages as pages
import routes.api as api
import routes.video as video


def create_app():
    app = Flask(__name__)

    # إنشاء الكاميرا مرة واحدة
    camera = CameraWorker(CAMERA_INDEX)

    # ربط الكاميرا بالـ routes
    pages.camera = camera
    api.camera = camera
    video.camera = camera

    # تسجيل الـ Blueprints
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(video_bp)

    return app, camera


if __name__ == "__main__":
    app, camera = create_app()

    # تشغيل الكاميرا مرة واحدة فقط
    camera.start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,          
        use_reloader=False,  
        threaded=True
    )
