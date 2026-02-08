from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import requests

BACKEND_URL = "http://127.0.0.1:5000"  # Change if your backend is hosted elsewhere

class SignupScreen(Screen):
    msg = StringProperty("")
    email_or_phone = StringProperty("")

    def request_otp(self):
        """Send or resend OTP to the current email/phone"""
        self.email_or_phone = self.ids.email_or_phone.text.strip()
        if not self.email_or_phone:
            self.msg = "Enter email or phone"
            return

        payload = {}
        if "@" in self.email_or_phone:
            payload["email"] = self.email_or_phone
        else:
            payload["phone"] = self.email_or_phone

        try:
            response = requests.post(f"{BACKEND_URL}/send-otp", json=payload)
            res = response.json()
            if res.get("status") == "success":
                self.msg = f"OTP sent to {self.email_or_phone}"
            else:
                self.msg = res.get("message", "Failed to send OTP")
        except Exception as e:
            self.msg = f"Error: {e}"

    def send_otp(self):
        """Called when pressing the Send OTP button"""
        self.request_otp()

    def resend_otp(self, *args):
        """Called when pressing the Resend OTP link"""
        self.request_otp()

    def verify_otp(self):
        otp = self.ids.otp_input.text.strip()
        if not otp:
            self.msg = "Enter OTP"
            return

        payload = {"otp": otp}
        if "@" in self.email_or_phone:
            payload["email"] = self.email_or_phone
        else:
            payload["phone"] = self.email_or_phone

        try:
            response = requests.post(f"{BACKEND_URL}/verify-otp", json=payload)
            res = response.json()
            if res.get("status") == "success":
                self.msg = "OTP verified! Proceed to create account"
                self.manager.current = "create_account"
                self.manager.get_screen("create_account").email_or_phone = self.email_or_phone
            else:
                self.msg = res.get("message", "Entered OTP is wrong. Try again.")
        except Exception as e:
            self.msg = f"Error: {e}"