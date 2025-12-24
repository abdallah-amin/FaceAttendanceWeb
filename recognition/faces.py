import numpy as np
import face_recognition

from config import TOLERANCE
from database.persons import get_all_persons


def encode_faces(image_rgb):
    """
    image_rgb: numpy array (RGB)
    returns:
        encodings: list of face encodings
        locations: face locations
    """
    locations = face_recognition.face_locations(image_rgb)
    encodings = face_recognition.face_encodings(image_rgb, locations)
    return encodings, locations


def match_face(encoding):
    """
    encoding: single face encoding
    returns:
        person (dict) or None
        distance (float) or None
    """
    persons = get_all_persons()

    if not persons:
        return None, None

    known_encodings = np.array([p["encoding"] for p in persons])

    distances = face_recognition.face_distance(known_encodings, encoding)
    best_idx = int(np.argmin(distances))
    best_dist = float(distances[best_idx])

    if best_dist < TOLERANCE:
        return persons[best_idx], best_dist

    return None, None
