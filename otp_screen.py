from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import requests 

class OTPScreen(Screen):
    msg = StringProperty("")
    email_value = StringProperty("")

    def verify_otp(self,otp):
        otp = self.ids.otp_input.text.strip()

        if not otp:
            self.msg = "Enter OTP"
            return

        try:
            res = requests.post("http://127.0.0.1:5000/verify-otp",
                                json={"email": self.email_value, "otp": otp})

            data = res.json()

            if data.get("status") == "success":
                self.manager.get_screen("create_account").email_value = entered_email
                self.manager.current = "create_account"

            else:
                self.msg = data.get("message", "Invalid OTP")
        except Exception as e:
            self.msg = str(e)

    def go_back(self):
        self.manager.current = "signup_email"

    def go_to_account(self):
        self.manager.current="create_account"
