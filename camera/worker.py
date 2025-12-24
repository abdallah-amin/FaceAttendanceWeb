import threading
import cv2

from attendance.service import mark_attendance
from recognition.faces import encode_faces, match_face


class CameraWorker:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.lock = threading.Lock()

        self.frame = None
        self.running = False

        # لمنع تكرار تسجيل الحضور
        self.seen_today = set()

        # آخر وجه Unknown (لاستخدامه في الإضافة من الكاميرا)
        self.last_unknown_encoding = None

        # تحسين الأداء
        self.frame_count = 0
        self.process_every_n_frames = 5   # كل كام فريم نعمل recognition
        self.last_results = []            # [(loc, text, color)]

    def start(self):
        # نفس إعدادات المشروع القديم (الأكثر استقرارًا)
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.cap.isOpened():
            raise RuntimeError("Camera could not be opened.")

        # مهم جدًا: تجهيز أول فريم قبل ما المتصفح يطلبه
        ok, frame = self.cap.read()
        if ok and frame is not None:
            with self.lock:
                self.frame = frame

        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            ok, frame = self.cap.read()
            if not ok or frame is None:
                continue

            disp = frame.copy()
            self.frame_count += 1

            # نعمل Face Recognition كل N فريم فقط
            if self.frame_count % self.process_every_n_frames == 0:
                small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

                encs, locs = encode_faces(rgb)
                new_results = []

                for face_enc, loc in zip(encs, locs):
                    person, dist = match_face(face_enc)

                    if person:
                        name = person["name"]
                        person_id = person["id"]
                        color = (0, 255, 0)
                        text = f"{name} {dist:.2f}"

                        if person_id not in self.seen_today:
                            mark_attendance(person_id)
                            self.seen_today.add(person_id)
                    else:
                        color = (0, 0, 255)
                        text = "Unknown"
                        self.last_unknown_encoding = face_enc

                    new_results.append((loc, text, color))

                # تحديث النتائج مرة واحدة (thread-safe)
                with self.lock:
                    self.last_results = new_results

            # نرسم آخر نتائج معروفة حتى في الفريمات اللي مفيهاش processing
            with self.lock:
                results = list(self.last_results)

            for loc, text, color in results:
                y1, x2, y2, x1 = [v * 4 for v in loc]
                cv2.rectangle(disp, (x1, y1), (x2, y2), color, 2)
                cv2.rectangle(disp, (x1, y2 - 30), (x2, y2), color, cv2.FILLED)
                cv2.putText(
                    disp,
                    text,
                    (x1 + 6, y2 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

            # تحديث الفريم المعروض
            with self.lock:
                self.frame = disp

    def get_jpeg(self):
        # ناخد نسخة من الفريم من غير ما نمسك الـ lock وقت الترميز
        with self.lock:
            frame = self.frame

        if frame is None:
            return None

        ok, buf = cv2.imencode(".jpg", frame)
        if not ok:
            return None

        return buf.tobytes()
