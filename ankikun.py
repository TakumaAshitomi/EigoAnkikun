from kivy.app import App
import japanize_kivy
from kivy.uix.widget import Widget

class MainScreen(Widget):
    pass
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)

class AnkikunApp(App):

    def __init__(self, **kwargs):
        super(AnkikunApp, self).__init__(**kwargs)
#        self.title = "英語暗記くん"

    def build(self):
        return  MainScreen()

if __name__ == "__main__":
    AnkikunApp().run()