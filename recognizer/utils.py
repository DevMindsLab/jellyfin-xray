import os
from PIL import Image

def split_trickplay_image(input_file, output_dir, columns=10, rows=7, start_time=0, step_seconds=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image = Image.open(input_file)
    width, height = image.size

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

    return count
