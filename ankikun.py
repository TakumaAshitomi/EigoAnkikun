from kivy.app import App
import japanize_kivy
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty, BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.popup import Popup

import re
import sqlite3
conn = sqlite3.connect("example.sqlite3")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS words(english text not null unique, translated text not null unique)''')

def checkAlnum(word):
  alnum = re.compile(r'^[a-zA-Z0-9]+$')
  result = alnum.match(word) is not None
  return result

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")
    obj_text2 = StringProperty("")
    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

class SuccessPopup(Popup):
    pass

class FailedPopup(Popup):
    pass

class ErrorPopup(Popup):
    pass

class QuizPopup(Popup):
    quiz_items = ListProperty([])
    quiz_items1 = StringProperty("")
    quiz_items2 = StringProperty("")
    def __init__(self, **kwargs):
        super(QuizPopup, self).__init__(**kwargs)
        c.execute('''SELECT * FROM words ORDER BY RANDOM() LIMIT 1''')
        row = c.fetchone()
        for col in row:
            self.quiz_items.append(col)
        self.quiz_items1 = self.quiz_items[0]
        self.quiz_items2 = self.quiz_items[1]
        
    def quiz_answer_press(self, quiz_item, answer):
        c.execute('''select translated from words where english=?''', (quiz_item,))
        quiz = c.fetchone()
        if quiz[0] == answer:
            popup = SuccessPopup()
        else:
            popup = FailedPopup()
            print(quiz)
        popup.open()

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        before_text = self.text
        self.text = txt
        try:
            if checkAlnum(before_text):
                c.execute('''update words set english=? where english=? ''', (txt,before_text))
            else:
                c.execute('''update words set translated=? where translated=? ''', (txt,before_text))
            conn.commit()
        except sqlite3.Error as e:
            popup = ErrorPopup()
            popup.open()

    def delete_word(self):
        text = self.text
        try:
            if checkAlnum(text):
                c.execute('''delete from words where english=? ''', (text,))
            else:
                c.execute('''delete from words where translated=? ''', (text,))
            conn.commit()
        except sqlite3.Error as e:
            popup = ErrorPopup()
            popup.open()

class ListScreen(Screen,BoxLayout,Widget):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        self.get_users()
    
    def get_users(self):
        c.execute('''SELECT english, translated FROM words''')
        rows = c.fetchall()
        for row in rows:
            for col in row:
                self.data_items.append(col)

    def quiz_on_press(self):
        popup = QuizPopup()
        popup.open()
    
class MainScreen(Screen,Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save_button(self):
        try:
            c.execute('''insert into words(english, translated) values(:english, :translated)''',{"english":self.englishword.text,"translated":self.translatedword.text})
            conn.commit()
        except sqlite3.Error as e:
            popup = ErrorPopup()
            popup.open()
   
class AnkikunApp(App):

    def __init__(self, **kwargs):
        super(AnkikunApp, self).__init__(**kwargs)
        self.title = "英語暗記くん"

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(ListScreen(name='sub'))
        return self.sm

if __name__ == "__main__":
    AnkikunApp().run()