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

    # En db/conexion_base.py, dentro de la clase ConexionBase

# ... (tus métodos conectar, cerrar, consultar...) ...

    def insertar_informacion(self, tabla, datos):
        """
        Ejecuta un INSERT en la tabla especificada con los datos del diccionario.
        Retorna el ID de la fila insertada o None en caso de error.
        
        :param tabla: Nombre de la tabla (ej: 'hotel.bloqueos_historial')
        :param datos: Diccionario {columna: valor}
        """
        if not datos:
            return None

        # Separar llaves (columnas) y valores
        columnas = datos.keys()
        valores = datos.values()
        
        # Crear placeholders: (%s, %s, %s)
        placeholders = ', '.join(['%s'] * len(datos))
        columnas_sql = ', '.join(columnas)

        # Crear la consulta INSERT
        consulta = f"""
            INSERT INTO {tabla} ({columnas_sql})
            VALUES ({placeholders})
            RETURNING id;
        """

        try:
            self.conectar()
            self.cursor.execute(consulta, tuple(valores))
            
            # 1. HACER COMMIT para hacer el cambio permanente (¡CLAVE!)
            self.conn.commit() 
            
            # 2. Obtener el ID que devuelve el RETURNING
            resultado = self.cursor.fetchone()
            return resultado if resultado else None
            
        except Exception as e:
            if hasattr(self, 'conn') and self.conn:
                self.conn.rollback() # Deshacer si hay error
            print(f"[ERROR] Escritura INSERT en {tabla}: {e}")
            return None
        finally:
            self.cerrar()

# En db/conexion_base.py, dentro de la clase ConexionBase

# ... (tus métodos insertar_informacion, consultar, etc.) ...

    def actualizar_informacion(self, tabla, datos, condicion_where):
        """
        Ejecuta un UPDATE genérico.
        :param tabla: Nombre de la tabla (ej: 'hotel.bloqueos_historial')
        :param datos: Diccionario {columna: valor} a actualizar
        :param condicion_where: Diccionario {columna: valor} para la cláusula WHERE
        """
        if not datos or not condicion_where:
            return None

        # Construir SET
        set_part = []
        valores_update = []
        for col, val in datos.items():
            set_part.append(f"{col} = %s")
            valores_update.append(val)
        
        # Construir WHERE
        where_part = []
        for col, val in condicion_where.items():
            where_part.append(f"{col} = %s")
            valores_update.append(val)
            
        consulta = f"""
            UPDATE {tabla}
            SET {', '.join(set_part)}
            WHERE {' AND '.join(where_part)};
        """
        
        try:
            self.conectar()
            self.cursor.execute(consulta, tuple(valores_update))
            self.conn.commit() # ¡COMMIT! Para que el Trigger se dispare.
            
            # Retorna el número de filas afectadas
            return self.cursor.rowcount
            
        except Exception as e:
            if hasattr(self, 'conn') and self.conn:
                self.conn.rollback()
            print(f"[ERROR] Escritura UPDATE en {tabla}: {e}")
            return None
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
            return True
        except Exception as e:
            print(f"[ERROR] PostgreSQL ejecutar_funcion {nombre_funcion}: {e}")
            return []
        finally:
            self.cerrar()
