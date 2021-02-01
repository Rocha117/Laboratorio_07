from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import psycopg2
from kivy.uix.screenmanager import SlideTransition
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.lang import Builder
from kivy.clock import Clock
import random
import Comandos
from kivy.uix.label import Label


rachita = "0"


class Pantalla1Window(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def nombre_label(self):
        txt = self.ids.NombreI.text
        self.ids.NombreL.text = txt

    def Crear_tabla():
        conn = None
        sql = """CREATE TABLE  jugador (
        nombre_jugador VARCHAR NOT NULL,
        puntaje_jugador INT NOT NULL)"""

        try:
            conn = psycopg2.connect(host="localhost",
                                    database="lab07",
                                    user="postgres",
                                    password="a",
                                    port="5432")
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    Crear_tabla()

    def submit(self, nombre_jugador, puntaje_jugador):
        sql = """ INSERT INTO jugador (nombre_jugador, puntaje_jugador) VALUES (%s, %s);"""
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="lab07",
                user="postgres",
                password="a",
                port="5432")
            cur = conn.cursor()

            # modificar puntuaciones
            cur.execute(sql, (nombre_jugador, puntaje_jugador))

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

    def datos_base(self):
        nomb = self.ids.NombreI.text
        puntaje = str(100)
        self.submit(nomb, puntaje)

    def next(self, *args):

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla02"


class Pantalla02(Screen):

    tiempo = NumericProperty(0)
    num1 = NumericProperty(0)
    num2 = NumericProperty(0)
    total = NumericProperty(0)
    inic = NumericProperty(0)
    racha = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flag_contador = False
        global rachita
        rachita = str(Pantalla02.racha)

    def iniciar(self):
        self.evento1 = Clock.schedule_once(self.numeros_aleatorios)
        self.contador = 5

        self.ids.racha.text = f"Racha: {self.racha}"
        if self.flag_contador == False:
            self.evento2 = Clock.schedule_interval(self.iniciar_contador, 1)
            self.flag_contador = True
        else:
            self.evento2.cancel()
            self.contador = 5
            self.evento2 = Clock.schedule_interval(self.iniciar_contador, 1)

    def enviar(self, suma):
        self.total = self.num1+self.num2

        if self.total == int(suma):
            self.flag_contador = True
            self.racha += 1
            self.iniciar()
            self.inic = self.total
        else:
            self.tiempo = 0
            self.contador = 0
            self.iniciar_contador
        self.ids.input.text = ''

    def numeros_aleatorios(self, dt):
        self.num1 = random.randint(1, 99)
        self.num2 = random.randint(1, 99)

    def iniciar_contador(self, dt):
        if self.contador > 0:
            self.tiempo = str(int(self.contador))
            self.contador -= 1
        else:
            self.ids.racha.text = "Fallaste :c"
            self.ids.mensaje.text = 'RESPONDA EN EL TIEMPO INDICADO:     0'
            self.ids.numeros.text = '----'

            self.en_racha = 0
            self.contador = 5
            self.next()

    def next(self, *args):

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla03"


class Pantalla03(Screen):

    def __init__(self, **kwargs):
        super(Pantalla03, self).__init__(**kwargs)
        self.name = "pantalla03"

    def añadir(self):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="lab07",
                user="postgres",
                password="a",
                port="5432")
            cur = conn.cursor()
            cur.execute("SELECT * FROM jugador;")
            rows = cur.fetchall()

            for row in rows:

                jugador_result = (row[0])
                puntaje_result = str(row[1])

                conn.commit()
                cur.close()

        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "** ERROR!!!!")
        finally:
            if conn is not None:
                conn.close()


class MyScreenManager(ScreenManager):
    pass


kv = Builder.load_file("pantalla1.kv")


class Pantalla1App(App):
    title = "Screen Manager"

    def build(self):
        return kv


if __name__ == '__main__':
    Pantalla1App().run()
