from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class CamaraWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CamaraApp(App):
    def build(self):
        return CamaraWindow()
        
if __name__ == '__main__':
    CamaraApp().run()