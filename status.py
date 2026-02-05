# status.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
from storage_manager import get_user_uploads


class StatusScreen(Screen):

    def on_pre_enter(self):
        Clock.schedule_once(lambda dt: self.update_list(), 0)
        Clock.schedule_interval(lambda dt: self.update_list(), 5)
    def on_leave(self):
        # ⛔ Stop auto refresh when leaving screen
        Clock.unschedule(self.update_list)
    def update_list(self):
        if not hasattr(self.ids, "upload_list"):
            return

        self.ids.upload_list.clear_widgets()

        app = App.get_running_app()
        username = app.user_data.get("username")

        # 🔹 LOAD ONLY THIS USER'S UPLOADS
        self.user_uploads = get_user_uploads(username)

        if not self.user_uploads:
            from kivy.uix.label import Label
            self.ids.upload_list.add_widget(Label(text="No uploads yet"))
            return

        for idx, item in enumerate(self.user_uploads):
            btn = Button(
                text=f"Track Upload {idx + 1}",
                size_hint_y=None,
                height=60,
                background_normal="",
                background_color=(1, 1, 1, 0.9),
                color=(0, 0, 0, 1),
                bold=True
            )
            btn.bind(on_release=lambda b, i=idx: self.goto_detail(i))
            self.ids.upload_list.add_widget(btn)

    def goto_detail(self, index):
        detail_screen = self.manager.get_screen("status_detail")
        detail_screen.show_detail(index)
        self.manager.current = "status_detail"

    def go_back(self):
        self.manager.current = "home"
