import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import StringProperty

#Window.size = (360, 640)
Window.fullscreen = True
DB_NAME = "wardrobe.db"

# Screens
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_main, 2)

    def switch_to_main(self, dt):
        self.manager.current = 'wardrobe_list'

class WardrobeListScreen(Screen):
    def on_pre_enter(self):
        self.load_wardrobes()

    def load_wardrobes(self):
        self.ids.wardrobe_container.clear_widgets()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS wardrobes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, age TEXT, photo_path TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            wardrobe_id INTEGER, name TEXT, item_count INTEGER)''')
        cursor.execute("SELECT id, name, age FROM wardrobes ORDER BY id DESC")
        for wid, name, age in cursor.fetchall():
            btn = Builder.load_string(f'''
Button:
    text: "{name}'s Wardrobe\\n({age})"
    size_hint_y: None
    height: 150
    on_release:
        app.root.get_screen('detail').load_categories({wid}, "{name}")
        app.root.current = 'detail'
''')
            self.ids.wardrobe_container.add_widget(btn)
        conn.close()

    def open_popup(self):
        AddWardrobePopup().open()

class WardrobeDetailScreen(Screen):
    wardrobe_name = StringProperty("Wardrobe Details")

    def load_categories(self, wardrobe_id, name):
        self.ids.category_container.clear_widgets()
        self.wardrobe_name = f"{name}'s Wardrobe"
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name, item_count FROM categories WHERE wardrobe_id=?", (wardrobe_id,))
        for cname, count in cursor.fetchall():
            btn = Builder.load_string(f'''
Button:
    text: "{cname} ({count})"
    size_hint_y: None
    height: 200
''')
            self.ids.category_container.add_widget(btn)
        conn.close()

class AddWardrobePopup(Popup):
    def add_wardrobe(self):
        name = self.ids.name_input.text.strip()
        age = self.ids.age_input.text.strip()
        photo = self.ids.photo_input.text.strip()

        if name:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO wardrobes (name, age, photo_path) VALUES (?, ?, ?)", (name, age, photo))
            wid = cursor.lastrowid

            default_categories = ['Accessories', 'Clothes', 'Footwear']
            for cat in default_categories:
                cursor.execute("INSERT INTO categories (wardrobe_id, name, item_count) VALUES (?, ?, ?)", (wid, cat, 0))

            conn.commit()
            conn.close()
            self.dismiss()
            App.get_running_app().root.get_screen('wardrobe_list').load_wardrobes()

# KV Layout
KV = '''
<AddWardrobePopup>:
    title: "Add New Wardrobe"
    size_hint: 1, 1
    #size: 320, 300
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        TextInput:
            id: name_input
            hint_text: "Baby Name"

        TextInput:
            id: age_input
            hint_text: "Age (e.g., 1 year 2 months)"

        TextInput:
            id: photo_input
            hint_text: "Photo path (optional)"

        Button:
            text: "Add"
            on_release: root.add_wardrobe()

        Button:
            text: "Cancel"
            on_release: root.dismiss()

ScreenManager:
    SplashScreen:
    WardrobeListScreen:
    WardrobeDetailScreen:

<SplashScreen>:
    name: 'splash'
    canvas.before:
        Rectangle:
            source: 'assets/splash_bg.jpg'
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        Image:
            source: 'assets/logo.png'
            allow_stretch: True
            keep_ratio: True

<WardrobeListScreen>:
    name: 'wardrobe_list'

    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10

        Label:
            text: "Wardrobe List"
            font_size: 64
            size_hint_y: None
            height: 60
            bold: True

        ScrollView:
            BoxLayout:
                id: wardrobe_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 10

        Button:
            text: "+ Add Wardrobe"
            size_hint_y: None
            height: 150
            on_release: root.open_popup()

<WardrobeDetailScreen>:
    name: 'detail'

    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10

            Button:
                text: "⬅ Back"
                size_hint_x: None
                width: 80
                on_release: app.root.current = 'wardrobe_list'

            Label:
                text: root.wardrobe_name
                font_size: 64
                bold: True

        ScrollView:
            BoxLayout:
                id: category_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 10
'''

Builder.load_string(KV)

class BabyWardrobeApp(App):
    def build(self):
        self.title = "Baby Wardrobe"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(WardrobeListScreen(name='wardrobe_list'))
        sm.add_widget(WardrobeDetailScreen(name='detail'))
        return sm

if __name__ == '__main__':
    BabyWardrobeApp().run()