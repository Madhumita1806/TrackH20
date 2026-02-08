from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
store = JsonStore("appdata.json")
class FrontPage(Screen):
    


    def go_to_login(self):
        self.manager.current = "login"
