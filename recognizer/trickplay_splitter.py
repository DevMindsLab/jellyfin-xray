import os
import re
from PIL import Image

def split_trickplay_image(input_file, output_dir, start_time=0, step_seconds=10):
    """Zerschneidet ein Trickplay-Mosaik in Einzelbilder basierend auf Ordnernamen oder Bildgröße."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image = Image.open(input_file)
    width, height = image.size

    # Versuche aus Verzeichnisname Spalten x Reihen zu extrahieren
    folder_name = os.path.basename(os.path.dirname(input_file))
    match = re.search(r"(\d+)\s*-\s*(\d+)x(\d+)", folder_name)
    if match:
        columns = int(match.group(2))
        rows = int(match.group(3))
    else:
        # Automatischer Fallback
        possible_columns = [5, 10, 12, 15, 16, 20]
        possible_rows = [5, 6, 7, 8, 10, 12]

        columns, rows = None, None
        for c in possible_columns:
            if width % c == 0:
                for r in possible_rows:
                    if height % r == 0:
                        columns, rows = c, r
                        break
                if columns and rows:
                    break
        if not columns or not rows:
            columns, rows = 10, 7  # finaler Notfall-Fallback

    tile_width = width // columns
    tile_height = height // rows

    count = 0
    for row in range(rows):
        for col in range(columns):
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height

            tile = image.crop((left, upper, right, lower))
            timestamp = start_time + (count * step_seconds)
            filename = os.path.join(output_dir, f"{timestamp:04d}.jpg")
            tile.save(filename)
            count += 1

    return {
        "success": True,
        "tiles_created": count,
        "layout": f"{columns}x{rows}",
        "output_dir": output_dir
    }