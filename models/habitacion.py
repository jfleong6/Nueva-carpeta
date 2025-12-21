from db.conexion_base import ConexionBase
import datetime
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

        # --- CORRECCIÓN CLAVE: AHORA SON 9 PARÁMETROS ---
        parametros = (
            # 1. p_numero (text)
            datos.get("numero"),
            # 2. p_tipo (text)
            datos.get("tipo"),
            # 3. p_capacidad (integer)
            int(datos.get("capacidad")),
            # 4. p_precio_noche (real)
            float(datos.get("precio_noche")),
            # 5. p_cama (integer)
            int(datos.get("cama", 0)),
            # 6. p_sencilla (integer)
            int(datos.get("sencilla", 0)),
            # 7. p_camarote (integer)
            int(datos.get("camarote", 0)),
            
            # 8. p_estado (text): Por defecto '1'. Lo convertimos a string.
            str(datos.get("estado", 1)), 
            
            # 9. p_activo (boolean): Asumimos True para una nueva habitación.
            True 
        ) # ¡LISTO! 9 parámetros enviados.

        # La línea self.cursor.execute(query, parametros) debería pasar ahora
        resultado = conn.ejecutar_funcion("hotel.insertar_habitacion", parametros)

        if resultado:
            print(f"[OK] Habitación {datos.get('numero')} agregada.")
            return {"ok": True, "mensaje": f"[OK] Habitación {datos.get('numero')} agregada."}

        return {"ok": False, "mensaje": "No se recibió respuesta del procedimiento"}

    except Exception as e:
        print(f"[ERROR] al agregar habitación: {e}")
        return {"ok": False, "error": str(e)}

def bloquear_habitacion(datos):
    """
    Registra un bloqueo. El Trigger en BD se encarga de cambiar el estado.
    Recibe: { "numero": "101", "usuario_id": 1, "motivo": "Pintura" }
    """
    try:
        print(f"[INFO] Bloqueando habitación: {datos}")
        numero_hab = datos.get('numero')
        
        # ---------------------------------------------------------
        # PASO 1: BUSCAR ID DE HABITACIÓN (Usando tu estilo de consulta)
        # ---------------------------------------------------------
        
        habitacion_id = datos.get('numero')# El ID numérico (int)
        # ---------------------------------------------------------
        # PASO 2: INSERTAR USANDO EL NUEVO MÉTODO GENÉRICO
        # ---------------------------------------------------------
        datos_insertar = {
            "habitacion_id": habitacion_id, # Usamos el ID encontrado (int)
            "usuario_id": int(datos.get("usuario_id", 1)),
            "motivo": datos.get("motivo"),
            "activo": True
        }
        
        id_bloqueo = conn.insertar_informacion(
            tabla="hotel.bloqueos_historial",
            datos=datos_insertar
        )
        print(id_bloqueo)
        if id_bloqueo:
            print(f"[OK] Bloqueo ID {id_bloqueo} registrado. Trigger activo.")
            return {"ok": True, "mensaje": f"Habitación {numero_hab} bloqueada exitosamente."}
        else:
            return {"ok": False, "error": "Fallo en la inserción de datos del historial"}

    except Exception as e:
        print(f"[ERROR] al bloquear habitación: {e}")
        return {"ok": False, "error": str(e)}
    
def desbloquear_habitacion(numero_habitacion, usuario_id=1):
    try:
        print(f"[INFO] Procesando desbloqueo para habitación: {numero_habitacion}")

        # 1. DEFINIR DATOS A ACTUALIZAR
        datos_actualizar = {
            "activo": False,
            # No es estrictamente necesario, pero es buena práctica para auditoría
            "fecha_fin": datetime.datetime.now()
        }

        # 3. DEFINIR CONDICIÓN WHERE
        condicion_where = {
            "habitacion_id": numero_habitacion,
            "activo": True # SOLO actualizar el que está ACTIVO
        }

        # 4. EJECUTAR UPDATE
        filas_afectadas = conn.actualizar_informacion(
            tabla="hotel.bloqueos_historial",
            datos=datos_actualizar,
            condicion_where=condicion_where
        )

        if filas_afectadas and filas_afectadas > 0:
            print(f"[OK] Bloqueo cerrado. El Trigger liberó la habitación.")
            return {"ok": True, "mensaje": f"Habitación {numero_habitacion} desbloqueada."}
        elif filas_afectadas == 0:
             return {"ok": False, "error": f"No se encontró un bloqueo activo para la habitación {numero_habitacion}."}
        else:
             return {"ok": False, "error": "Fallo en la conexión de la base de datos."}

    except Exception as e:
        print(f"[ERROR] al desbloquear habitación: {e}")
        return {"ok": False, "error": str(e)}
    
# En models/habitaciones.py (o donde manejes las consultas de habitaciones)

def obtener_detalle_habitacion(numero_habitacion):
    """
    Obtiene todos los detalles de una habitación, incluyendo el historial de aseo.
    """
    try:      
                
        habitacion_id = numero_habitacion

        # 2. Obtener datos básicos de la habitación
        query_hab = """
            SELECT 
                h.numero, h.tipo, h.capacidad, h.precio_noche, 
                h.cama, h.sencilla, h.camarote, h.estado, h.fecha_ultimo_aseo
            FROM hotel.habitaciones h
            WHERE h.id = %s
        """
        # La función consultar debe devolver un formato usable (lista de dicts o tuplas)
        detalle_hab = conn.consultar(query_hab, (habitacion_id,))
        
        if not detalle_hab:
            return {"ok": False, "error": "Error al obtener detalles"}

        # 3. Obtener los últimos 5 registros de aseo
        query_aseo = """
            SELECT 
                fecha_inicio, fecha_fin, duracion_minutos, observaciones, tipo_aseo, u.nombre
            FROM hotel.aseo_historial ah
            LEFT JOIN core.usuarios u ON ah.usuario_id = u.id
            WHERE ah.habitacion_id = %s
            ORDER BY fecha_inicio DESC
            LIMIT 5;
        """
        historial_aseo = conn.consultar(query_aseo, (habitacion_id,))
        
        # 4. Combinar y devolver los datos
        datos_combinados = {
            "habitacion": detalle_hab[0], # Asumiendo que es una lista de un solo diccionario/registro
            "historial_aseo": historial_aseo
        }
        
        return {"ok": True, "data": datos_combinados}

    except Exception as e:
        print(f"[ERROR] al obtener detalle de habitación: {e}")
        return {"ok": False, "error": str(e)}

def marcar_disponible(id_hab, numero_habitacion, usuario):
    try:
        # 1. Obtener el ID de la habitación
        habitacion_id = id_hab
        print(type(habitacion_id))
        
        # 2. Actualizar el estado a '1' (Disponible)
        # Esto dispara el Trigger de FIN DE ASEO
        query_update = """
            UPDATE hotel.habitaciones 
            SET estado = '1'
            WHERE id = %s AND estado = '3' -- Solo se actualiza si está en Limpieza
            RETURNING id;
        """
        result = conn.ejecutar(query_update, (habitacion_id,))
        
        
        if result == 0:
            return {"ok": False, "mensaje": f"Habitación {numero_habitacion} no estaba en estado de limpieza (3) o no existe."}
        conn.commit()
        return {"ok": True, "mensaje": f"Habitación {numero_habitacion} marcada como disponible. Aseo auditado."}

    except Exception as e:
        print(f"[ERROR] al marcar disponible: {e}")
        return {"ok": False, "mensaje": f"Error al procesar la disponibilidad: {str(e)}"}
    finally:
        if conn:
            conn.cerrar()
            

def marcar_aseo(numero_habitacion, usuario_id):
    try:
        
        if not conn.conectar():
            raise Exception("Fallo la conexión a la base de datos.")
            
        # 1. Obtener el ID interno de la habitación (la API recibe el número)
        query_id = "SELECT id FROM hotel.habitaciones WHERE numero = %s"
        res_id = conn.consultar(query_id, (numero_habitacion,))
        
        if not res_id:
            return {"ok": False, "mensaje": f"Habitación {numero_habitacion} no encontrada."}
        
        habitacion_id = res_id[0]['id'] 

        # 2. Ejecutar el UPDATE que dispara el Trigger de INICIO DE ASEO
        # Condición: El estado NO debe ser ya '3' (para evitar registros duplicados) 
        # y NO debe ser '0' (Bloqueada), ya que un bloqueo tiene prioridad.
        query_update = """
            UPDATE hotel.habitaciones 
            SET estado = '3'
            WHERE id = %s 
              AND estado IS DISTINCT FROM '3'
              AND estado IS DISTINCT FROM '0'
            RETURNING id;
        """
        result = conn.ejecutar(query_update, (habitacion_id,)) 
        
        if result == 0:
            conn.rollback() 
            return {"ok": False, "mensaje": f"Habitación {numero_habitacion} no pudo cambiar de estado (ya estaba en Limpieza o Bloqueada)."}

        # 3. Guardar los cambios
        conn.commit() 
        
        return {"ok": True, "mensaje": f"Habitación {numero_habitacion} marcada para limpieza. Historial iniciado."}

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERROR] al marcar aseo: {e}")
        return {"ok": False, "mensaje": f"Error al procesar el cambio a aseo: {str(e)}"}
    finally:
        if conn:
            conn.cerrar()
