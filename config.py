from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "Images_Attendance"
MODELS_DIR = ROOT / "models"
ENC_PATH = MODELS_DIR / "known_faces.npz"
ATT_CSV = ROOT / "Attendance.csv"

CAMERA_INDEX = 0
TOLERANCE = 0.6
