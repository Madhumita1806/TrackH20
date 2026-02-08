from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import os
from datetime import datetime
import geocoder
from geopy.geocoders import Nominatim
import requests

class CameraScreen(Screen):

    def on_enter(self):
        # Start camera
        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self):
        # Stop camera
        Clock.unschedule(self.update)
        if self.cap:
            self.cap.release()

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Keep original for saving
        self.original_frame = frame.copy()

        # Rotate preview for natural view
        preview_frame = cv2.rotate(frame, cv2.ROTATE_180)

# Convert BGR → RGB (VERY IMPORTANT)
        preview_frame = cv2.cvtColor(preview_frame, cv2.COLOR_BGR2RGB)

        buf = preview_frame.tobytes()
        texture = Texture.create(size=(preview_frame.shape[1], preview_frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

        self.ids.camera_preview.texture = texture

        

    def take_photo(self):
        frame = self.original_frame

        # -------- GET LOCATION --------
        g = geocoder.ip('me')
        lat, lon = None, None
        place = "Location not available"
        if g.ok:
            lat, lon = g.latlng
            geolocator = Nominatim(user_agent="geo_capture")
            location = geolocator.reverse(f"{lat}, {lon}", language="en")
            if location:
                place = location.address

        # -------- ADD LOCATION TEXT --------
        img = frame.copy()
        y = img.shape[0] - 60
        if lat and lon:
            cv2.putText(img, f"Lat: {lat:.6f}, Lon: {lon:.6f}",
                        (10, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            y += 20
        cv2.putText(img, f"Place: {place}",
                    (10, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

        # -------- SAVE IMAGE LOCALLY --------
        folder = "uploaded_images"
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = f"captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(folder, filename)
        cv2.imwrite(filepath, img)

        # -------- SEND TO UPLOAD SCREEN --------
        upload_screen = self.manager.get_screen("upload")
        upload_screen.image_path = filepath
        upload_screen.ids.preview.source = filepath
        upload_screen.ids.preview.reload() 
        

        # -------- UPLOAD TO BACKEND --------
       
        # Return to upload screen
        self.manager.current = "upload"
