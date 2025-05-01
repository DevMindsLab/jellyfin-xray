import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
DEFAULT_TRICKPLAY_PATH = "data/trickplay/"

# .env einlesen
load_dotenv(dotenv_path=ENV_PATH)

def get_people_path():
    return os.getenv("JELLYFIN_PEOPLE_PATH", "/var/lib/jellyfin/metadata/People/")

def get_trickplay_path():
    return os.getenv("TRICKPLAY_PATH", DEFAULT_TRICKPLAY_PATH)

def set_trickplay_path(new_path):
    lines = []
    updated = False

    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                if line.startswith("TRICKPLAY_PATH="):
                    lines.append(f"TRICKPLAY_PATH={new_path}\n")
                    updated = True
                else:
                    lines.append(line)

    if not updated:
        lines.append(f"TRICKPLAY_PATH={new_path}\n")

    with open(ENV_PATH, "w") as f:
        f.writelines(lines)

    os.environ["TRICKPLAY_PATH"] = new_path