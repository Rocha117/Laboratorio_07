from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import psycopg2

class Pantalla1Window(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def nombre_label(self):
        txt = self.ids.NombreI.text
        self.ids.NombreL.text = txt.title()
    
    def insert_jugador(self, nombre_jugador, puntaje_jugador):
        sql = """
        INSERT INTO jugadores(nombre_jugador, puntaje_jugador) VALUES (%s, %s);
        """
        conn = None
        try:
                conn = psycopg2.connect(
                    host = "localhost",
                    port = "5432",
                    user = "postgres",
                    database = "Usuarios",
                    password = "Clevex"
                    )

                cur = conn.cursor()
                cur.execute(sql, (nombre_jugador, puntaje_jugador))
                conn.commit()
                cur.close()

                if conn is not None:
                    conn.close()
                print("Datos guardados\n")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
    
    def datos_base(self):
        nomb = self.ids.NombreI.text.title()
        puntaje = 100
        self.insert_jugador(nomb, puntaje)
    
    def jugar(self):
        self.datos_base()
        pass


class Pantalla1App(App):
    def build(self):

        return Pantalla1Window()

if __name__=='__main__':
    Pantalla1App().run()