import sqlite3
import urllib.parse
from uuid import UUID

# 🔧 Konfiguration
db_path = "/home/rene/PycharmProjects/jellyfin-xray/library.db"
jellyfin_url = "http://myflix.home:8096/web/#/details?id=0de6c444-e7e1-8357-afb6-82bd5d99db9e"

def extract_guid_from_url(url):
    """Extrahiert die GUID aus einer Jellyfin-Detail-URL."""
    parsed = urllib.parse.urlparse(url)
    fragment = parsed.fragment

    if "?" in fragment:
        _, query_str = fragment.split("?", 1)
    elif "&" in fragment or "=" in fragment:
        query_str = fragment
    else:
        return None

    query = urllib.parse.parse_qs(query_str)
    return query.get("id", [None])[0]

def get_movie_metadata_from_guid(db_path, guid_str):
    """Gibt Titel, Jahr und Schauspielerliste zu einem Eintrag anhand seiner GUID zurück."""
    try:
        guid_blob = UUID(guid_str).bytes_le  # 🧠 Richtige Byte-Reihenfolge für Jellyfin!
    except (ValueError, AttributeError):
        return {
            "success": False,
            "message": f"❌ Ungültige GUID: '{guid_str}'"
        }

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Name, ProductionYear FROM TypedBaseItems
        WHERE Guid = ?
    """, (guid_blob,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {
            "success": False,
            "message": f"❌ Kein Eintrag mit GUID '{guid_str}' gefunden."
        }

    title, year = row

    cursor.execute("""
        SELECT Name FROM People
        WHERE ItemId = ?
    """, (guid_blob,))
    actors = [r[0] for r in cursor.fetchall()]
    conn.close()

    return {
        "success": True,
        "title": title,
        "year": year,
        "actors": actors
    }

# 👉 Testlauf
guid = extract_guid_from_url(jellyfin_url)
if guid:
    data = get_movie_metadata_from_guid(db_path, guid)
    if data["success"]:
        print(f"🎬 {data['title']} ({data['year']}) mit {len(data['actors'])} Schauspielern:")
        for actor in data["actors"]:
            print(" -", actor)
    else:
        print(data["message"])
else:
    print("❌ Keine GUID in URL gefunden.")