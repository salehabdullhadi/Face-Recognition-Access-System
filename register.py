# register.py
import cv2
import os
from tkinter import simpledialog, messagebox
import tkinter as tk

def register_user():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    username = simpledialog.askstring("Register", "Enter new username:")
    if not username:
        messagebox.showerror("Error", "Username cannot be empty.")
        return

    user_dir = os.path.join("face_data", username)
    os.makedirs(user_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Webcam not accessible.")
        return

    messagebox.showinfo("Info", "Press 's' to save face image, 'q' to quit.")

    image_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Capture Face - Press 's' to save, 'q' to quit", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            image_count += 1
            img_path = os.path.join(user_dir, f"image_{image_count}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"[SAVED] Image saved to {img_path}")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Done", f"✔ Saved {image_count} images for user '{username}'.")
