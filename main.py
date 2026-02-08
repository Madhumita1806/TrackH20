from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.storage.jsonstore import JsonStore

# Import all screens
from front import FrontPage
from login import LoginScreen
from signup import SignupScreen
from otp_screen import OTPScreen
from profile_screen import ProfileScreen
from homescreen import HomeScreen
from create_account import CreateAccountScreen
from upload import UploadScreen
from status import StatusScreen
from statusdetails import StatusDetailScreen
from ml_predict import is_water_waste 
# Local backend
from backend import backend
from camera import CameraScreen

store = JsonStore("userdata.json")


class MyManager(ScreenManager):
    pass


class MyApp(MDApp):
    user_data = {}
    user_profile = {}  # {'username': 'Kaviya', 'mobile': '9876543210'}

    

    # ---------------- SET USER INFO GLOBALLY ----------------
    def set_user(self, username, mobile):
        self.user_data["username"] = username
        self.user_data["mobile"] = mobile

    # ---------------- BUILD APP ----------------
    def build(self):
        self.sm = MyManager()
        Builder.load_file("main.kv")

        # Add screens
        self.sm.add_widget(FrontPage(name="front"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(SignupScreen(name="signup"))
        self.sm.add_widget(OTPScreen(name="otp"))
        self.sm.add_widget(CreateAccountScreen(name="create_account"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(UploadScreen(name="upload"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(StatusScreen(name="status"))
        self.sm.add_widget(StatusDetailScreen(name="status_detail"))
        self.sm.add_widget(CameraScreen(name="camera"))

        return self.sm

    # ---------------- UNIVERSAL BACK BUTTON ----------------
    def go_back(self):

        # “screen_name” : “go_back_to_this_screen”
        back_map = {
            "login": "front",
            "signup": "login",
            "otp": "signup",
            "create_account": "signup",
            "profile": "home",
            "upload": "home",
            "status": "home",
            "status_detail": "status"
        }

        current = self.root.current

        # If mapping available → use it
        if current in back_map:
            self.root.current = back_map[current]
        else:
            # Default fallback
            self.root.current = "front"
    

    def on_image_upload(image_path):
        if is_water_waste(image_path):
            print("Uploading image...")
        else:
            print("Please upload correct water-waste image")



if __name__ == "__main__":
    MyApp().run()
