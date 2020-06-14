from kivy.app import App
import japanize_kivy
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

class ListScreen(Screen,Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MainScreen(Screen,Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def wordlist_button(self):
        self.clear_widgets()
        return ListScreen()

    def save_button(self):
        return
        

class AnkikunApp(App):

    def __init__(self, **kwargs):
        super(AnkikunApp, self).__init__(**kwargs)
#        self.title = "英語暗記くん"

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(ListScreen(name='sub'))
        return self.sm

if __name__ == "__main__":
    AnkikunApp().run()