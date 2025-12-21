from flask import Blueprint, render_template, request, jsonify
from models.habitacion import *


hotel_bp = Blueprint('hotel', __name__)

@hotel_bp.route("/hotel")
def vista_hotel():
    return render_template("hotel/vista_hotel.html")

@hotel_bp.route("/vista_habitaciones")
def vista_habitaciones():
    habitaciones = obtener_habitaciones()
    habitaciones_ordenadas = sorted(habitaciones, key=lambda h: h["numero"])
    return render_template("hotel/vista_habitaciones.html",habitaciones=habitaciones_ordenadas)

@hotel_bp.route("/huespedes")
def vista_huespedes():
    return render_template("hotel/vista_huespedes.html")

@hotel_bp.route("/reservas")
def reservas():
    return render_template("hotel/vista_reservas.html")    

@hotel_bp.route("/gastos")
def vista_gastos():
    return render_template("hotel/vista_gastos.html")

@hotel_bp.route("/inventario")
def vista_inventario():
    return render_template("hotel/vista_inventario.html")

@hotel_bp.route("/arqueo")
def vista_arqueo():
    return render_template("hotel/vista_arqueo.html")

@hotel_bp.route("/gestion_habitaciones")
def gestion_habitaciones():
    habitaciones = obtener_habitaciones()
    habitaciones_ordenadas = sorted(habitaciones, key=lambda h: h["numero"])
    return render_template("hotel/gestion_habitaciones.html", habitaciones=habitaciones_ordenadas)

@hotel_bp.route("/habitacion/<int:numero>")
def habitacion_detalle(numero):
    habitacion = obtener_habitaciones(numero)
    if not habitacion:
        return "Habitación no encontrada", 404
    return render_template("hotel/partials/registro_huesped.html", habitacion=habitacion)


@hotel_bp.route("/gestion_habitaciones_movil/<usuario>")
def gestion_habitaciones_movil(usuario):
    # habitaciones = obtener_habitaciones_asignadas(usuario)
    return render_template("hotel/gestion_habitaciones_movil.html")#, habitaciones=habitaciones)

@hotel_bp.route("/reporte_limpieza/<fecha>")
def reporte_limpieza(fecha):
    # datos = generar_reporte_limpieza(fecha)
    return render_template("hotel/reporte_limpieza.html" )#, datos=datos)


@hotel_bp.route("/api/habitaciones/agregar", methods=["POST"])
def agregarHabitacion():
    try:
        datos = request.get_json(force=True)

        respuesta = agregar_habitacion(datos=datos)
        print(respuesta)
        # Convertimos el string en booleano real por si acaso
        ok = respuesta.get('ok', "")
        # print(ok)
        if ok:
            return jsonify({"ok":True,"mensaje": "Habitacion Guardada"}), 200
        else:
            return jsonify({"error": respuesta.get("error", "Error desconocido")}), 400

    except Exception as e:
        print(f"[ERROR] en endpoint agregarHabitacion: {e}")
        return jsonify({"error": str(e)}), 500


# RUTA PARA BLOQUEAR
@hotel_bp.route("/api/bloquear", methods=["POST"])
def bloquearHabitacionRoute():
    try:
        # force=True evita errores si el header no es application/json
        datos = request.get_json(force=True) 
        
        # Llamamos a tu lógica estilo "ConexionBase"
        respuesta = bloquear_habitacion(datos)
        
        if respuesta.get("ok"):
            return jsonify(respuesta), 200
        else:
            return jsonify(respuesta), 400
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# RUTA PARA DESBLOQUEAR (Para el botón del candado abierto 🔓)
@hotel_bp.route("/api/desbloquear", methods=["POST"])
def desbloquearHabitacionRoute():
    try:
        datos = request.get_json(force=True)
        numero = datos.get("numero")
        
        respuesta = desbloquear_habitacion(numero)
        
        if respuesta.get("ok"):
            return jsonify(respuesta), 200
        else:
            # Usamos 400 si el problema es lógico (no estaba bloqueada)
            return jsonify(respuesta), 400 
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    

@hotel_bp.route('/api/habitaciones/detalle/<string:numero>', methods=['GET'])
def get_detalle_habitacion(numero):
    resultado = obtener_detalle_habitacion(numero)
    
    if resultado["ok"]:
        return jsonify(resultado["data"]), 200
    else:
        return jsonify({"error": resultado["error"]}), 404


@hotel_bp.route('/api/marcar_limpia', methods=['POST'])
def api_marcar_limpia():
    data = request.get_json()
    
    numero = data.get('numero')
    id_hab = data.get('id_hab')
    
    # CRÍTICO: Aquí debes obtener el ID del usuario logueado de tu sistema de sesión.
    # Por ahora, usamos un ID fijo para que el Trigger funcione en la auditoría.
    usuario_id = data.get('usuario')
    
    if not numero:
        return jsonify({"ok": False, "error": "Número de habitación requerido"}), 400

    resultado = marcar_disponible(id_hab,numero, usuario_id)

    if resultado["ok"]:
        return jsonify({"ok": True, "mensaje": resultado["mensaje"]}), 200
    else:
        # Devolvemos el error específico para que el Front-end lo muestre
        return jsonify({"ok": False, "error": resultado["mensaje"]}), 500
    
@hotel_bp.route('/api/marcar_aseo', methods=['POST'])
def api_marcar_aseo():
    data = request.get_json()
    
    numero = data.get('numero')
    
    # CRÍTICO: Aquí debes obtener el ID del usuario logueado de tu sistema de sesión.
    # Usamos un ID fijo '1' como valor de prueba para la auditoría.
    usuario_id = 1 
    
    if not numero:
        return jsonify({"ok": False, "error": "Número de habitación requerido"}), 400

    resultado = marcar_aseo(numero, usuario_id)

    if resultado["ok"]:
        return jsonify({"ok": True, "mensaje": resultado["mensaje"]}), 200
    else:
        # Devolver el error específico para que el Front-end lo muestre
        return jsonify({"ok": False, "error": resultado["mensaje"]}), 500