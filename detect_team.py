# detect_team.py
import face_recognition
import cv2
import os

def load_all_encodings(data_dir="face_data"):
    encodings = []
    names = []

    for user in os.listdir(data_dir):
        user_folder = os.path.join(data_dir, user)
        for img_file in os.listdir(user_folder):
            img_path = os.path.join(user_folder, img_file)
            image = face_recognition.load_image_file(img_path)
            face_encs = face_recognition.face_encodings(image)
            for enc in face_encs:
                encodings.append(enc)
                names.append(user)
    return encodings, names


def check_team_presence():
    known_encodings, known_names = load_all_encodings()
    if not known_encodings:
        print("[ERROR] No registered users found.")
        return

    cap = cv2.VideoCapture(0)
    print("[INFO] Scanning... Press 'q' to quit.")
    recognized = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            min_distance = min(distances)
            best_match_index = distances.tolist().index(min_distance)

            if min_distance < 0.45:
                name = known_names[best_match_index]
                recognized.add(name)
            else:
                name = "Not in the team"

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Team Presence - Press 'q' to Quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n🧑‍🤝‍🧑 Team Members Present:")
    for name in recognized:
        print(f"✅ {name}")
