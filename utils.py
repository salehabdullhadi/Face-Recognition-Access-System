# utils.py
import os
import cv2
import face_recognition
import numpy as np

def load_user_encodings(username):
    user_folder = os.path.join("face_data", username)
    if not os.path.exists(user_folder):
        return []

    encodings = []
    for file in os.listdir(user_folder):
        img_path = os.path.join(user_folder, file)
        image = face_recognition.load_image_file(img_path)
        face_encs = face_recognition.face_encodings(image)
        if face_encs:
            encodings.append(face_encs[0])
    return encodings

def recognize_user(username):
    known_encodings = load_user_encodings(username)
    if not known_encodings:
        print("[ERROR] No encodings found for this user.")
        return False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Camera not available.")
        return False

    print("[INFO] Show your face to the camera...")
    match_found = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            for face_encoding in face_encodings:
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                min_distance = min(distances)
                if min_distance < 0.45:
                    print(f"[MATCH] Face distance: {min_distance:.4f} ✅")
                    match_found = True
                    break
                else:
                    print(f"[NO MATCH] Closest distance: {min_distance:.4f} ❌")
        else:
            print("[INFO] No face detected in frame.")

        cv2.imshow("Login - Press 'q' to quit", frame)
        if match_found or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return match_found
