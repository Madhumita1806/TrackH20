from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from plyer import camera, filechooser
import json
import os

PROFILE_JSON = "userdata.json"

class ProfileScreen(Screen):
    profile_photo_path = StringProperty("")

    def built(self):
        self.profile_photo_path = ""
        return Builder.load_file("main.kv")

    # ---------------- POPUP METHOD ----------------
    def show_popup(self, text):
        popup = Popup(
            title="Info",
            content=Label(text=text),
            size_hint=(None, None),
            size=(400, 250)
        )
        popup.open()

    # ---------------- CAMERA ----------------
    def open_camera(self):
        try:
            camera.take_picture(
                filename="trackh2o_camera.jpg",
                on_complete=self.camera_complete
            )
        except Exception as e:
            self.show_popup(f"Camera Error: {e}")

    def camera_complete(self, path):
        if path:
            self.profile_photo_path = path
            self.ids.profile_photo.source = self.profile_photo_path
            self.ids.profile_photo.reload()
            self.show_popup("Photo Captured")

    # ---------------- GALLERY ----------------
    def open_gallery(self):
        try:
            filechooser.open_file(on_selection=self.gallery_complete)
        except Exception as e:
            self.show_popup(f"Gallery Error: {e}")

    def gallery_complete(self, selection):
        if selection:
            self.profile_photo_path = selection[0]
            try:
                self.ids.profile_photo.source = self.profile_photo_path
                self.ids.profile_photo.reload()
            except:
                self.show_popup("Error updating profile picture")
            self.show_popup("Image Selected")

    # ---------------- DROPDOWN ----------------
    def open_user_type_menu(self):
        caller = self.ids.user_type
        items = [
            {"text": t, "viewclass": "OneLineListItem",
             "on_release": lambda x=t: self.set_user_type(x)}
            for t in [
                "Citizen Reporter",
                "Volunteer / Community Worker",
                "Municipal Staff / Cleanup Team",
                "NGO Member",
                "Admin (restricted)"
            ]
        ]

        from kivymd.uix.menu import MDDropdownMenu
        self.menu_user = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4,
            position="auto"
        )
        self.menu_user.open()

    def set_user_type(self, value):
        self.ids.user_type.text = value
        self.menu_user.dismiss()

    # ---------------- SUBMIT PROFILE ----------------
    def submit_form(self):
        try:
            # Collect data
            data = {
                "fullname": self.ids.fullname.text.strip(),
                "email": self.ids.email.text.strip(),
                "mobile": self.ids.mobile.text.strip(),
                "city": self.ids.city.text.strip(),
                "state": self.ids.state.text.strip(),
                "pincode": self.ids.pincode.text.strip(),
                "user_type": self.ids.user_type.text.strip(),
                "profile_photo": self.profile_photo_path
            }

            # Validation
            if not data["fullname"] or not data["email"] or not data["mobile"]:
                self.show_popup("Please fill all required fields!")
                return

            # Load existing profiles
            profiles = []
            if os.path.exists(PROFILE_JSON):
                try:
                    with open(PROFILE_JSON, "r") as f:
                        profiles = json.load(f)
                        if not isinstance(profiles, list):
                            profiles = []
                except:
                    profiles = []

            # Add new profile
            profiles.append(data)

            # Save to JSON
            with open(PROFILE_JSON, "w") as f:
                json.dump(profiles, f, indent=4)

            # Update app globals
            app = App.get_running_app()
            app.user_profile = {
                "username": data["fullname"],
                "mobile": data["mobile"]
            }
            app.user_data = {
                "username": data["fullname"],
                "mobile": data["mobile"]
            }

            # Navigate to home
            app.root.current = "home"
            self.show_popup("Profile submitted successfully!")

        except Exception as e:
            self.show_popup(f"Failed to submit profile: {e}")
