import face_recognition

# Lade die zu testenden Frames
frame_0410 = face_recognition.load_image_file("/home/rene/PycharmProjects/data/trickplay/Jurassic World/Jurassic World 2015.trickplay/xray/0410.jpg")
frame_10100 = face_recognition.load_image_file("/home/rene/PycharmProjects/data/trickplay/Jurassic World/Jurassic World 2015.trickplay/xray/10100.jpg")

# Lade den bekannten Schauspieler aus folder.jpg
actor_img = face_recognition.load_image_file("/home/rene/PycharmProjects/data/People/B/Bryce Dallas Howard/folder.jpg")
actor_enc = face_recognition.face_encodings(actor_img)[0]


# Führe Erkennung im Frame durch
def test_frame(image, label):
    face_locs = face_recognition.face_locations(image)
    encs = face_recognition.face_encodings(image, face_locs)
    print(f"🔍 {label}: {len(encs)} Gesicht(er) gefunden")

    for i, enc in enumerate(encs):
        match = face_recognition.compare_faces([actor_enc], enc, tolerance=0.7)[0]
        print(f"   ➜ Gesicht {i + 1}: Match mit Bryce? {'✅ JA' if match else '❌ NEIN'}")


# Teste beide Bilder
test_frame(frame_0410, "0410.jpg")
test_frame(frame_10100, "10100.jpg")
