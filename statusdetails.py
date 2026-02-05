# statusdetails.py
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
from storage_manager import get_user_uploads
from kivy.app import App
import requests

class StatusDetailScreen(Screen):
    selected_index = NumericProperty(0)

    def on_pre_enter(self):
        # Schedule refresh every 5 seconds
        self._event = Clock.schedule_interval(self.refresh_status, 5)

    def on_leave(self):
        if hasattr(self, "_event"):
            self._event.cancel()

    def show_detail(self, index):
        self.selected_index = index
        self.update_ui(fetch_latest=True)

    def refresh_status(self, dt=None):
        self.update_ui(fetch_latest=True)

    def update_ui(self, fetch_latest=False):
        app = App.get_running_app()
        username = app.user_data.get("username")
        if not username:
            return

        # Load user uploads
        if fetch_latest:
            try:
                r = requests.get("http://127.0.0.1:5000/get-data")
                if r.status_code == 200:
                    uploads = [u for u in r.json() if u.get("uploaded_by") == username]
                else:
                    uploads = get_user_uploads(username)
            except Exception as e:
                print("Error fetching status:", e)
                uploads = get_user_uploads(username)
        else:
            uploads = get_user_uploads(username)

        if self.selected_index >= len(uploads):
            return

        item = uploads[self.selected_index]

        # Update UI
        self.ids.img_preview.source = item.get("image_path", "")
        self.ids.desc_label.text = f"Description: {item.get('description', 'No description')}"

        status_colors = {
            "Pending": (1, 0.8, 0, 1),
            "On process": (0, 0.5, 1, 1),
            "Completed": (0, 1, 0, 1)
        }
        self.ids.status_label.text = f"Status: {item.get('status', 'Pending')}"
        self.ids.status_label.color = status_colors.get(item.get("status"), (0, 0, 0, 1))

    def go_back(self):
        self.manager.current = "status"
