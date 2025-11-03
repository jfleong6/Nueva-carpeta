from flask import Blueprint, render_template, request, jsonify
from models.habitacion import *
from db.conexion_base import ConexionBase


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

