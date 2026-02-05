import os
import json
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.snackbar import Snackbar
from werkzeug.security import check_password_hash
from kivy.app import App
from storage_manager import get_user_uploads

USERS_FILE = "users.json"       # Stores username and hashed password
USERDATA_FILE = "userdata.json" # Stores profile info including mobile

class LoginScreen(Screen):
    msg = StringProperty("")  # For showing messages in KV

    def login(self, button_instance=None):
        """Login function called from KV on button press."""
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if not username or not password:
            self.msg = "Enter username and password!"
            Snackbar(text=self.msg).open()
            return

        if not os.path.exists(USERS_FILE):
            self.msg = "User database not found!"
            Snackbar(text=self.msg).open()
            return

        # --- Load users.json ---
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            users = data.get("users", [])

        # --- Find user by username ---
        user_found = None
        for user in users:
            if user.get("username") == username:
                user_found = user
                break

        if not user_found:
            self.msg = "Username not found!"
            Snackbar(text=self.msg).open()
            return

        # --- Verify password ---
        if not check_password_hash(user_found.get("password"), password):
            self.msg = "Incorrect password!"
            Snackbar(text=self.msg).open()
            return

        # --- Fetch mobile from userdata.json ---
        mobile = ""
        if os.path.exists(USERDATA_FILE):
            with open(USERDATA_FILE, "r") as f:
                profiles = json.load(f)
                for profile in profiles:
                    # Match by username
                    if profile.get("fullname") == username:
                        mobile = profile.get("mobile", "")
                        break

        # --- Save user info globally in App ---
        app = App.get_running_app()
        app.user_data = {
            "username": username,
            "mobile": mobile
        }

        # --- Login successful ---
        self.msg = "Login Successful!"
        Snackbar(text=self.msg).open()
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.manager.current = "home"
        self.msg = ""

    def on_login_success(self, username):
        uploads = get_user_uploads(username)

        for upload in uploads:
            self.display_image(upload["image_path"])

    def go_to_forgot(self):
        """Navigate to forgot password screen."""
        self.manager.current = "forgot"

    def go_to_signup(self):
        """Navigate to signup screen."""
        self.manager.current = "signup"
