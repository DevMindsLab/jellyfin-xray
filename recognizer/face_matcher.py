import os
import json
import face_recognition
import shutil
import datetime
from recognizer.trickplay_splitter import split_trickplay_image
from config import get_trickplay_path
from config import get_people_path

XRAY_OUTPUT_FILE = "output/xray.json"
KNOWN_ACTORS_PATH = get_people_path()

def load_known_faces():
    if not os.path.exists(KNOWN_ACTORS_PATH):
        raise FileNotFoundError(f"Pfad zu den Schauspielern nicht gefunden: {KNOWN_ACTORS_PATH}")

    known_faces = []
    for root, dirs, files in os.walk(KNOWN_ACTORS_PATH):
        if "folder.jpg" in files:
            actor_name = os.path.basename(root)
            img_path = os.path.join(root, "folder.jpg")
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_faces.append({
                    "name": actor_name,
                    "encoding": encodings[0]
                })

    if not known_faces:
        raise FileNotFoundError("Keine gültigen Schauspielerbilder gefunden.")

    return known_faces

def analyze_trickplay():
    trickplay_dir = get_trickplay_path()
    xray_dir = os.path.join(trickplay_dir, "xray")
    os.makedirs(xray_dir, exist_ok=True)

    try:
        known_faces = load_known_faces()
    except FileNotFoundError as e:
        return {
            "success": False,
            "message": str(e)
        }

    result = {}

    if not os.path.isdir(trickplay_dir):
        return {"success": False, "message": f"Trickplay-Verzeichnis {trickplay_dir} nicht gefunden."}

    # Prüfen ob Neuschnitt nötig ist
    needs_splitting = not os.listdir(xray_dir)
    if not needs_splitting:
        trick_files = []
        for root, _, files in os.walk(trickplay_dir):
            for f in files:
                if f.lower().endswith((".jpg", ".jpeg", ".png")):
                    trick_files.append(os.path.join(root, f))
        if trick_files:
            latest_xray = max([os.path.getmtime(os.path.join(xray_dir, f)) for f in os.listdir(xray_dir)], default=0)
            for trick_path in trick_files:
                if os.path.getmtime(trick_path) > latest_xray:
                    needs_splitting = True
                    break

    # Neu zerschneiden
    if needs_splitting:
        shutil.rmtree(xray_dir)
        os.makedirs(xray_dir)
        counter = 0
        for root, _, files in os.walk(trickplay_dir):
            for file in sorted(files):
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    input_file = os.path.join(root, file)
                    try:
                        split_trickplay_image(input_file, xray_dir, start_time=counter * 1000)
                        counter += 1
                    except Exception as e:
                        print(f"⚠️ Fehler beim Zerschneiden von {input_file}: {e}")

    # Analyse
    for file in sorted(os.listdir(xray_dir)):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        filepath = os.path.join(xray_dir, file)
        try:
            image = face_recognition.load_image_file(filepath)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
        except Exception:
            continue  # falls Bild beschädigt o. ä.

        frame_results = []
        for encoding in face_encodings:
            for known in known_faces:
                if face_recognition.compare_faces([known["encoding"]], encoding, tolerance=0.75)[0]:
                    frame_results.append(known["name"])
                    break

        timestamp = os.path.splitext(file)[0]
        result[timestamp] = frame_results

    os.makedirs(os.path.dirname(XRAY_OUTPUT_FILE), exist_ok=True)
    with open(XRAY_OUTPUT_FILE, "w") as f:
        json.dump({
            "analyzed_at": datetime.datetime.now().isoformat(),
            "frames": result
        }, f, indent=2)

    return {
        "success": True,
        "message": f"{len(result)} Bilder analysiert",
        "frames": len(result),
        "actors_detected": len(set(a for r in result.values() for a in r))
    }