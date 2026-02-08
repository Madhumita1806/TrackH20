from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.image import Image


Window.clearcolor = (0.85, 0.93, 1, 1)  # water blue

class HoverButton(ButtonBehavior, BoxLayout):
    def __init__(self, text='', icon='', bg_color_value=(1, 1, 1, 1), **kwargs):

        # REMOVE bg_color_value from kwargs BEFORE calling super()
        # (this is the important part)
        self.bg_color_value = bg_color_value

        # NOW it is safe to call super
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 10
        self.size_hint = (None, None)
        self.size = (170, 150)

        # Hover color slightly darker
        self.hover_color = (
            bg_color_value[0] * 0.9,
            bg_color_value[1] * 0.9,
            bg_color_value[2] * 0.9,
            1
        )

        # Icon
        self.icon = Image(
            source=icon,
            size_hint=(1, 0.75),
            allow_stretch=True
        )

        # Label
        self.label = Label(
            text=text,
            font_size="18sp",
            bold=True,
            color=(0, 0.2, 0.4, 1),
            size_hint=(1, 0.35),
            halign="center"
        )
        self.label.bind(size=self.label.setter("text_size"))

        self.add_widget(self.icon)
        self.add_widget(self.label)

        # Background rectangle
        with self.canvas.before:
            self.bg_color = Color(*self.bg_color_value)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

        self.bind(pos=self.update_rect, size=self.update_rect)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_mouse_pos(self, *args):
        _, pos = args
        if self.collide_point(*pos):
            self.bg_color.rgba = self.hover_color
        else:
            self.bg_color.rgba = self.bg_color_value



class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.85, 0.93, 1, 1)   # Light Aqua Blue
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

        root = BoxLayout(orientation="vertical")
        self.add_widget(root)

        # =========================
        # Top Bar
        # =========================
        topbar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=75,
            padding=[15, 10], spacing=10
        )

        with topbar.canvas.before:
            Color(0.0, 0.48, 0.95, 1)
            self.top_rect = Rectangle(pos=topbar.pos, size=topbar.size)
        topbar.bind(pos=self.update_top_rect, size=self.update_top_rect)

        dropdown = DropDown()
        for opt in ["About", "User Profile", "Settings", "Logout"]:
            btn = Button(text=opt, size_hint_y=None, height=40)
            if opt == "Settings":
                btn.bind(on_release=self.go_to_settings)
            
            if opt == "Logout":
                btn.bind(on_release=self.go_to_login)
            dropdown.add_widget(btn)

        hamburger = Button(
            text="☰", font_size="50sp", size_hint_x=None, width=80,
            background_color=(0, 0, 0, 0), color=(1, 1, 1, 1)
        )
        hamburger.bind(on_release=lambda btn: dropdown.open(btn))

        title = Label(
            text="[b]TrackH[sub]2[/sub]O[/b]", markup=True,
            color=(1, 1, 1, 1), font_size="34sp", halign="center"
        )
        title.bind(size=title.setter("text_size"))

        topbar.add_widget(hamburger)
        topbar.add_widget(title)
        topbar.add_widget(Widget(size_hint_x=None, width=40))

        root.add_widget(topbar)

        # =========================
        # Middle Section
        # =========================
        mid = BoxLayout(orientation="vertical", spacing=20)
        root.add_widget(mid)

        mid.add_widget(Widget(size_hint_y=0.15))

        heading = Label(
            text="[b]Welcome Back![/b]", markup=True,
            font_size="22sp", halign="center",
            color=(0, 0.25, 0.45, 1),
            size_hint_y=None, height=30
        )
        mid.add_widget(heading)

        mid.add_widget(Widget(size_hint_y=0.1))

        # Row 1 – Two Buttons
        row1 = BoxLayout(
            orientation="horizontal",
            spacing=25, size_hint=(None, None), height=170,
            width=400,           # width for 2 buttons
            pos_hint={"center_x": 0.5}
        )

        upload_btn = HoverButton("Upload Sample", "icons/upload.jpeg",bg_color_value=(0.85, 0.93, 1, 1))
        upload_btn.bind(on_release=self.go_to_upload)

        trace_btn = HoverButton("reports", "icons/reports.jpeg",bg_color_value=(0.85, 0.93, 1, 1))

        row1.add_widget(upload_btn)
        row1.add_widget(trace_btn)
        mid.add_widget(row1)

        # Row 2 – One Centered Button
        # Row 2 – One Centered Button
        row2 = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None), height=170
        )

        row2.add_widget(Widget(size_hint_x=.25))

        status_btn = HoverButton("View Status", "icons/status.jpeg", bg_color_value=(0.85, 0.93, 1, 1))
        status_btn.bind(on_release=self.go_to_status)  # Bind click to go to UploadScreen
        row2.add_widget(status_btn)

        row2.add_widget(Widget(size_hint_x=.25))
        mid.add_widget(row2)

        

        mid.add_widget(Widget(size_hint_y=0.3))

    def update_top_rect(self, instance, value):
        self.top_rect.pos = instance.pos
        self.top_rect.size = instance.size 

    def go_to_upload(self, instance):
        self.manager.current = "upload"

    def go_to_status(self, instance):
        self.manager.current = "status"

    def go_to_settings(self, instance):
        self.manager.current = "settings"
    def go_to_login(self, instance):
        self.manager.current = "front"

    def update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

