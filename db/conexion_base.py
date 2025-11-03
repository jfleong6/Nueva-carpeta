import psycopg2
from psycopg2.extras import RealDictCursor

class ConexionBase:
    def __init__(self, host="localhost", user="", password="", database=""):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def conectar(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a PostgreSQL: {e}")

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None

    def consultar(self, consulta, parametros=()):
        """Ejecuta un SELECT y retorna los resultados como lista de diccionarios"""
        try:
            self.conectar()
            self.cursor.execute(consulta, parametros)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] PostgreSQL consultar: {e}")
            return []
        finally:
            self.cerrar()

    def ejecutar_funcion(self, nombre_funcion, parametros=()):
        """
        Ejecuta una función de PostgreSQL.
        Retorna los resultados del SELECT dentro de la función.
        """
        try:
            self.conectar()
            # Postgres: SELECT * FROM funcion(param1, param2, ...)
            placeholders = ", ".join(["%s"] * len(parametros))
            query = f"SELECT * FROM {nombre_funcion}({placeholders});"
            self.cursor.execute(query, parametros)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] PostgreSQL ejecutar_funcion {nombre_funcion}: {e}")
            return []
        finally:
            self.cerrar()
