from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
import requests
import re

BACKEND_URL = "http://127.0.0.1:5000"

class CreateAccountScreen(Screen):
    msg = StringProperty("")
    email_or_phone = StringProperty("")

    # For real-time strength checking
    has_upper = BooleanProperty(False)
    has_lower = BooleanProperty(False)
    has_digit = BooleanProperty(False)
    has_special = BooleanProperty(False)

    strength_value = NumericProperty(0)   # 0 to 100 for progress bar

    def check_password_live(self, password):
        """Live update bullet points + bar"""
        self.has_upper = len(re.findall(r"[A-Z]", password)) >= 1
        self.has_lower = len(re.findall(r"[a-z]", password)) >= 1
        self.has_digit = len(re.findall(r"[0-9]", password)) >= 2
        self.has_special = len(re.findall(r"[!@#$%^&*()_+\-=\[\]{};':\",.<>/?]", password)) >= 1

        # Calculate strength
        count = sum([
            self.has_upper,
            self.has_lower,
            self.has_digit,
            self.has_special
        ])

        self.strength_value = count * 25  # 4 checks → 25% each

    def validate_password(self, password):
        if len(password) < 8:
            return "Password must be minimum 6 characters"

        if not self.has_upper:
            return "Password must contain at least 1 uppercase letters"
        if not self.has_lower:
            return "Password must contain at least 1 lowercase letters"
        if not self.has_digit:
            return "Password must contain at least 2 digits"
        if not self.has_special:
            return "Password must contain at least 1 special symbols"

        return None

    def create_account(self, username, password):
        if not username or not password:
            self.msg = "Username and password required"
            return

        validation_msg = self.validate_password(password)
        if validation_msg:
            self.msg = validation_msg + "\nExample: ABcd12@#"
            return

        payload = {"username": username, "password": password}

        if self.email_or_phone:
            if "@" in self.email_or_phone:
                payload["email"] = self.email_or_phone
            else:
                payload["phone"] = self.email_or_phone

        try:
            response = requests.post(f"{BACKEND_URL}/create-account", json=payload)
            res = response.json()

            if response.status_code == 201:
                self.msg = "Account created successfully!"
                self.manager.current = "profile"
            else:
                self.msg = res.get("message", "Account creation failed")

        except Exception as e:
            self.msg = f"Error: {e}"