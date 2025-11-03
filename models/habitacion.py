from db.conexion_base import ConexionBase

# Inicializas la conexión
conn = ConexionBase(user="postgres", password="jhonm320429", database="sistema")

def obtener_habitaciones(habitacion=None):
    try:
        if habitacion:
            query = "SELECT * FROM hotel.habitaciones WHERE numero = %s"
            return conn.consultar(query, (str(habitacion),))
        else:
            query = "SELECT * FROM hotel.habitaciones"
            return conn.consultar(query)
    except Exception as e:
        print(f"[ERROR] al obtener habitaciones: {e}")
        return []

def agregar_habitacion(datos):
    try:
        print(f"[INFO] Insertando habitación: {datos}")

        campos_obligatorios = ["numero", "tipo", "capacidad", "precio_noche"]
        for campo in campos_obligatorios:
            if not datos.get(campo):
                return {"ok": False, "error": f"Falta el campo obligatorio: {campo}"}

        parametros = (
            datos.get("numero"),
            datos.get("tipo"),
            int(datos.get("capacidad")),
            float(datos.get("precio_noche")),
            int(datos.get("cama", 0)),
            int(datos.get("sencilla", 0)),
            int(datos.get("camarote", 0))
        )

        resultado = conn.ejecutar_funcion("hotel.insertar_habitacion", parametros)

        if resultado and isinstance(resultado, list):
            fila = resultado[0]
            mensaje = fila.get("mensaje") if isinstance(fila, dict) else fila[0]
            print(f"[OK] Habitación {datos.get('numero')} agregada.")
            return {"ok": True, "mensaje": mensaje}

        return {"ok": False, "mensaje": "No se recibió respuesta del procedimiento"}

    except Exception as e:
        print(f"[ERROR] al agregar habitación: {e}")
        return {"ok": False, "error": str(e)}
