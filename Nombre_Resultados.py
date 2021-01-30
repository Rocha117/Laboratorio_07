import psycopg2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition

class Screen_Datos(Screen):
    def __init__(self, **kwargs):
        super(Screen_Datos, self).__init__(**kwargs)
    
        lblN=Label(text="INGRESE SU NOMBRE", font_size=25, size_hint=(.2,.1), pos=(350,370))

        self.txtN=TextInput(font_size=35, background_normal="", size_hint=(.4,.1), pos=(270,300))

        btnN=Button(text="OK", font_size=25, size_hint=(.2,.1), pos=(350,200))
        btnN.bind(on_press=self.submit)
        btn_next=Button(text="NEXT", font_size=15, size_hint=(.1,.05), pos=(710,10))
        btn_next.bind(on_press=self.next)

        fl1=FloatLayout(size=(200, 300))

        fl1.add_widget(lblN)
        fl1.add_widget(self.txtN)
        fl1.add_widget(btnN)
        fl1.add_widget(btn_next)

        self.add_widget(fl1)

    def next(self, *args):

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current="pantalla3"


    def submit(self, obj):

        sql= """ INSERT INTO jugador (nombre_jugador, puntaje_jugador) VALUES (%s, %s);"""
        conn=None
        try:
            conn=psycopg2.connect(
                host="localhost",
                database="lab07",
                user="postgres",
                password="ladymendoza_prograII",
                port="5432")
            cur=conn.cursor()

            cur.execute(sql, (self.txtN.text, 65))#modificar puntuaciones
            
            conn.commit()
            cur.close()
            if conn is not None:
                conn.close()

            print("todo bien")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "** ERROR!!!!")
        finally:
            if conn is not None:
                conn.close()
        
class Screen_Resultados(Screen):
    def __init__(self, **kwargs):
        super(Screen_Resultados, self).__init__(**kwargs)
        

        btn_next=Button(text="NEXT", font_size=15, size_hint=(.1,.05), pos=(710,10))
        btn_next.bind(on_press=self.next)
        

        fl1=FloatLayout(size=(200, 300))
        fl1.add_widget(btn_next)
        self.add_widget(fl1)
       
        
        conn = None
        try:
            conn=psycopg2.connect(
                host="localhost",
                database="lab07",
                user="postgres",
                password="ladymendoza_prograII",
                port="5432")
            cur=conn.cursor()
            cur.execute("SELECT * FROM jugador;")

            row = cur.fetchone()

            grid=GridLayout(cols=2)

            lbl_n=Label(text="Nombre", font_size=25)
            lbl_p=Label(text="Puntaje", font_size=25)

            grid.add_widget(lbl_n)
            grid.add_widget(lbl_p)

            self.add_widget(grid)

            while row is not None:
                grid=GridLayout(cols=2)

                jugador_result=(row[0])
                puntaje_result=str(row[1])

                lbl1=Label(text=jugador_result, font_size=20)
                lbl2=Label(text=puntaje_result, font_size=20)

                grid.add_widget(lbl1)
                grid.add_widget(lbl2)

                self.orientation=("vertical")
                self.add_widget(grid)

                row = cur.fetchone()

            conn.commit()

            cur.close()

            if conn is not None:
                conn.close()
            print("todo bien")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "** ERROR!!!!")
        finally:
            if conn is not None:
                conn.close()
    def next(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()

class ScreenApp(App):
    title="Screen Manager"
    def build(self):
        root = ScreenManager()

        root.add_widget(Screen_Datos())
        root.add_widget(Screen_Resultados(name="pantalla3"))

        return root

if __name__=="__main__":
    ScreenApp().run()