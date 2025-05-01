# Jellyfin X-Ray (Offline Plugin)

**Version:** Entwicklungsstand Alpha – Modulstruktur stabil, Integration vorbereitet  
**Autor:** Rene B.  
**Ziel:** Zeigt während der Wiedergabe in Jellyfin automatisch an, **welche Schauspieler in welcher Szene** zu sehen sind – ganz ähnlich wie Amazon X-Ray, aber vollständig **offline** und lokal.

---

## 🔧 Funktionsweise

Dieses Plugin verarbeitet **Trickplay-Bilder**, die Jellyfin generiert (ca. alle 10 Sekunden ein Bild).  
Es analysiert diese Bilder mit Hilfe von Gesichtserkennung und ordnet bekannte Schauspieler zu.  
Die Ergebnisse werden als `xray.json` gespeichert und können später z. B. im Jellyfin-Frontend live angezeigt werden.

---

## 📁 Projektstruktur (Kurzfassung)

```
jellyfin-xray/
├── main.py                  # Flask-Webinterface (Einstellungen, Analyse-Button)
├── config.py                # Pfad-Konfigurationen (Trickplay, People-Ordner)
├── recognizer/
│   ├── face_matcher.py      # Hauptlogik: Bilder analysieren, Gesichter erkennen
│   ├── utils.py             # Bild-Zerschneiden (split_trickplay_image)
│   ├── people_filter.py     # GUID aus URL → Schauspieler abrufen (noch Teststand)
├── output/                  # Ergebnis-Ordner pro Film/Serie
│   └── xray.json            # Analyseergebnis (timestamp → Schauspieler)
├── library.db               # Lokale Kopie der Jellyfin-Datenbank
├── requirements.txt         # Python-Abhängigkeiten
```

---

## 🧠 Aktueller Stand (01.05.2025)

| Modul              | Status  | Beschreibung |
|--------------------|---------|--------------|
| Trickplay-Splitter | ✅ Fertig | Zerlegt Bilder in Einzel-Frames (alle 10 Sekunden) |
| Gesichtsanalyse    | ✅ Fertig | Erkennt Schauspieler mit `face_recognition` |
| Schauspielerfilter | ✅ Fertig | GUID → relevante Schauspieler aus `library.db` |
| Web-GUI (Flask)    | ✅ Fertig | Optionen-Formular + Analyse starten |
| Live-Zusammenführung | 🟡 Offen | Schauspielerfilter wird noch nicht von `face_matcher` verwendet |

---

## 📥 Nutzung

### Voraussetzungen

- Jellyfin mit aktivierten Trickplay-Bildern
- Ordnerstruktur mit `folder.jpg`-Bildern pro Schauspieler
- Python 3.9+
- Abhängigkeiten: siehe `requirements.txt`

```bash
pip install -r requirements.txt
```

### Start der Weboberfläche

```bash
python main.py
```

→ erreichbar unter `http://localhost:5000/options`

Dort: Trickplay-Pfad setzen → „Analysieren“ klicken

---

## 🧩 Geplante Weiterentwicklung

- [ ] Filterlogik mit `get_movie_metadata_from_guid()` direkt in `face_matcher` nutzen
- [ ] JSON-Dateien pro GUID statt global
- [ ] Frontend: Overlay-Anzeige während Wiedergabe (Jellyfin Plugin)
- [ ] GUI: Film aus Liste auswählen statt manuelle GUID
- [ ] Performance-Optimierung (Parallele Bildverarbeitung)

---

## 🛠️ Entwicklerhinweise

- Die Gesichtserkennung basiert auf `face_recognition` und benötigt jeweils ein gutes `folder.jpg` pro Schauspieler (gesichtszentriert).
- GUIDs müssen aus Jellyfin-URLs im Fragment (`#`) extrahiert werden – die Funktion dafür ist in `people_filter.py` enthalten.
- Für Zuverlässigkeit ist `UUID(...).bytes_le` nötig (Little-Endian!).

---

## Lizenz

Dieses Projekt ist derzeit in privater Entwicklung. Geplante Open-Source-Freigabe unter MIT-Lizenz.
