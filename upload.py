import os
import json
import requests
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from plyer import filechooser, camera
from backend import backend
from datetime import datetime
from ml_predict import is_water_waste
from storage_manager import save_user_upload


# ------------------ PATHS ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploaded_images")
UPLOAD_FILE = os.path.join(BASE_DIR, "uploads.json")

REMOTE_URL = "http://localhost:5000/export-data"  # Remote endpoint

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ------------------ JSON HANDLING ------------------
def load_uploads():
    if not os.path.exists(UPLOAD_FILE):
        return []
    try:
        with open(UPLOAD_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_uploads(data):
    with open(UPLOAD_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ UPLOAD SCREEN ------------------
class UploadScreen(Screen):
    image_path = StringProperty("")

    # --------- FILE CHOOSER ---------
    def select_image(self):
        file = filechooser.open_file(filters=[("Images", "*.png;*.jpg;*.jpeg")])
        if file:
            self.image_path = file[0]
            self.ids.preview.source = self.image_path

    # --------- OPEN CAMERA ---------
    def open_camera(self):
        try:
            filename = os.path.join(UPLOAD_FOLDER, "captured_image.jpg")
            camera.take_picture(filename, self.camera_callback)
        except Exception as e:
            self.show_message(f"Camera error: {e}")

    def camera_callback(self, filepath):
        if filepath:
            self.image_path = filepath
            self.ids.preview.source = filepath

    # --------- SUBMIT DATA ---------
    def submit_data(self):
        desc = self.ids.desc.text.strip()

        if not self.image_path or not desc:
            self.show_message("Please select an image and enter description!")
            return

        if not is_water_waste(self.image_path):
            Popup(
                title="Invalid Image",
                content=Label(text="Please upload correct water-waste image"),
                size_hint=(0.8, 0.4)
            ).open()
            return

        # --------- GET USER INFO ---------
        app = App.get_running_app()
        username = getattr(app, "user_data", {}).get("username", "")
        mobile = getattr(app, "user_data", {}).get("mobile", "")

        if not username:
            self.show_message("User not logged in!")
            return

        # --------- SAVE IMAGE LOCALLY ---------
        filename = os.path.basename(self.image_path)
        saved_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            with open(self.image_path, "rb") as src:
                with open(saved_path, "wb") as dst:
                    dst.write(src.read())
        except Exception as e:
            self.show_message(f"Image save failed: {e}")
            return

        # --------- SAVE PERMANENTLY PER USER (ONLY ADDITION) ---------
        save_user_upload(
            user_id=username,
            username=username,
            image_file_path=saved_path,
            geo_location={
                "latitude": 0.0,
                "longitude": 0.0
            }
        )

        # --------- LOAD OLD UPLOADS ---------
        uploads = load_uploads()

        # --------- CREATE CLEAN ENTRY ---------
        entry = {
            "id": len(uploads) + 1,
            "uploaded_by": username,
            "mobile": mobile,
            "description": desc,
            "image": filename,
            "image_path": saved_path,   # ✅ FIXED LINE
            "status": "Pending",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # --------- SAVE TO JSON ---------
        uploads.append(entry)
        save_uploads(uploads)

        # --------- UPDATE BACKEND ---------
        backend.uploads.append(entry)

        # --------- SEND TO SERVER ---------
        try:
            resp = requests.post(REMOTE_URL, json=entry)
            print("Remote Response:", resp.status_code, resp.text)
        except Exception as e:
            print("Error sending to server:", e)

        # --------- RESET UI ---------
        self.ids.preview.source = ""
        self.ids.desc.text = ""
        self.image_path = ""

        self.show_message("Submitted Successfully!")

    # --------- POPUP MESSAGE ---------
    def show_message(self, text):
        popup = Popup(
            title="Info",
            content=Label(text=text),
            size_hint=(None, None),
            size=(400, 250)
        )
        popup.open()

    # --------- GO BACK ---------
    def go_back(self):
        self.manager.current = "home"
