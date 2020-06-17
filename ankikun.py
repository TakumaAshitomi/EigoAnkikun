from kivy.app import App
import japanize_kivy
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
import sqlite3
conn = sqlite3.connect("example.sqlite3")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS words(id int PRIMARY KEY, english text, translated text)''')

class ListScreen(Screen,BoxLayout,Widget):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        self.get_users()
    
    def get_users(self):
        c.execute('''SELECT english, translated FROM words''')
        rows = c.fetchall()
        #data_itemsに値を入れる
        for row in rows:
            for col in row:
                self.data_items.append(col)

class MainScreen(Screen,Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save_button(self):
        c.execute('''insert into words(english, translated) values(:english, :translated)''',{"english":self.englishword.text,"translated":self.translatedword.text})
        conn.commit()
        #for row in c.execute('''select * from words'''):

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