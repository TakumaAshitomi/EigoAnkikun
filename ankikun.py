from kivy.app import App
import japanize_kivy

class AnkikunApp(App):

    def __init__(self, **kwargs):
        super(AnkikunApp, self).__init__(**kwargs)
        self.title = "英語暗記くん"
        self.text = "こんにちは世界"

if __name__ == "__main__":
    AnkikunApp().run()