from flask import Flask, render_template, request, redirect
from config import get_trickplay_path, set_trickplay_path
from recognizer.face_matcher import analyze_trickplay
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "web", "templates")  # Das ist neu

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route("/options", methods=["GET"])
def options():
    return render_template("options.html", current_path=get_trickplay_path())

@app.route("/save_options", methods=["POST"])
def save_options():
    path = request.form.get("trickplay_path")
    set_trickplay_path(path)
    return redirect("/options")

@app.route("/analyze", methods=["POST"])
def analyze():
    result = analyze_trickplay()  # Gibt Dict mit success/message zurück
    return render_template("options.html", current_path=get_trickplay_path(), status=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)