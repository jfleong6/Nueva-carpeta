-- ===========================================================
-- 🏨 MÓDULO HOTEL - ESTRUCTURA DE BASE DE DATOS (PostgreSQL)
-- Autor: Fredy
-- Adaptado por ChatGPT
-- ===========================================================

-- Crear base de datos si no existe
-- CREATE DATABASE hotel_db;
\c hotel;

-- ===========================================================
-- TABLA: habitaciones
-- ===========================================================
CREATE TABLE IF NOT EXISTS habitaciones (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(20) UNIQUE,
    tipo VARCHAR(50),
    capacidad INT,
    precio_noche NUMERIC(10,2),
    cama SMALLINT DEFAULT 0,
    sencilla SMALLINT DEFAULT 0,
    camarote SMALLINT DEFAULT 0,
    estado VARCHAR(10) DEFAULT '1',  -- 1 libre, 2 ocupada, 3 reservada
    activo BOOLEAN DEFAULT TRUE
);

-- ===========================================================
-- TABLA: grupos_hotel
-- ===========================================================
CREATE TABLE IF NOT EXISTS grupos_hotel (
    id SERIAL PRIMARY KEY,
    nombre_grupo VARCHAR(100),
    tipo_cuenta VARCHAR(20) CHECK (tipo_cuenta IN ('grupal','individual')) NOT NULL
);

-- ===========================================================
-- TABLA: reservas_hotel
-- ===========================================================
CREATE TABLE IF NOT EXISTS reservas_hotel (
    id SERIAL PRIMARY KEY,
    cliente_id INT,
    habitacion_id INT REFERENCES habitaciones(id),
    grupo_id INT REFERENCES grupos_hotel(id),
    fecha_entrada TIMESTAMP,
    fecha_salida TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'reservada' CHECK (estado IN ('reservada','confirmada','cancelada')),
    total NUMERIC(10,2)
);

-- ===========================================================
-- TABLA: registro_huesped
-- ===========================================================
CREATE TABLE IF NOT EXISTS registro_huesped (
    id SERIAL PRIMARY KEY,
    reserva_id INT REFERENCES reservas_hotel(id),
    nombre_completo VARCHAR(100),
    tipo_documento VARCHAR(20),
    numero_documento VARCHAR(30),
    nacionalidad VARCHAR(50),
    fecha_nacimiento DATE,
    sexo VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_ingreso TIMESTAMP,
    fecha_salida TIMESTAMP,
    es_principal BOOLEAN DEFAULT FALSE,
    observaciones TEXT
);

-- ===========================================================
-- TABLA: consumos_hotel
-- ===========================================================
CREATE TABLE IF NOT EXISTS consumos_hotel (
    id SERIAL PRIMARY KEY,
    reserva_id INT REFERENCES reservas_hotel(id),
    producto_id INT,
    cantidad INT,
    precio_unitario NUMERIC(10,2),
    fecha TIMESTAMP
);

-- ===========================================================
-- TABLA: ventas_hotel
-- ===========================================================
CREATE TABLE IF NOT EXISTS ventas_hotel (
    id SERIAL PRIMARY KEY,
    reserva_id INT REFERENCES reservas_hotel(id),
    cliente_id INT,
    usuario_id INT,
    total NUMERIC(10,2),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(30) DEFAULT 'completada'
);

-- ===========================================================
-- TABLA: detalle_venta_hotel
-- ===========================================================
CREATE TABLE IF NOT EXISTS detalle_venta_hotel (
    id SERIAL PRIMARY KEY,
    venta_id INT REFERENCES ventas_hotel(id),
    producto_id INT,
    cantidad INT,
    precio_unitario NUMERIC(10,2)
);

-- ===========================================================
-- TABLA: pagos_hotel
-- ===========================================================
CREATE TABLE IF NOT EXISTS pagos_hotel (
    id SERIAL PRIMARY KEY,
    venta_id INT REFERENCES ventas_hotel(id),
    tipo_pago_id INT,
    monto NUMERIC(10,2),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================================
-- TABLA: movimientos_inventario_hotel
-- ===========================================================
CREATE TABLE IF NOT EXISTS movimientos_inventario_hotel (
    id SERIAL PRIMARY KEY,
    producto_id INT,
    tipo VARCHAR(10) CHECK (tipo IN ('entrada','salida','traslado')),
    cantidad INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    referencia VARCHAR(100)
);

-- ===========================================================
-- TABLA: servicios_combo
-- ===========================================================
CREATE TABLE IF NOT EXISTS servicios_combo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL,
    es_por_persona BOOLEAN DEFAULT TRUE
);

-- ===========================================================
-- TABLA: servicios_combo_detalle
-- ===========================================================
CREATE TABLE IF NOT EXISTS servicios_combo_detalle (
    id SERIAL PRIMARY KEY,
    combo_id INT NOT NULL REFERENCES servicios_combo(id) ON DELETE CASCADE,
    beneficio TEXT NOT NULL,
    orden INT DEFAULT 1
);

-- ===========================================================
-- TABLA: servicios_combo_asignado
-- ===========================================================
CREATE TABLE IF NOT EXISTS servicios_combo_asignado (
    id SERIAL PRIMARY KEY,
    registro_huesped_id INT NOT NULL REFERENCES registro_huesped(id),
    combo_id INT NOT NULL REFERENCES servicios_combo(id),
    cantidad_personas INT DEFAULT 1,
    precio_total NUMERIC(10,2) NOT NULL
);

-- ===========================================================
-- VISTA: cargar_habitaciones
-- ===========================================================
CREATE OR REPLACE VIEW cargar_habitaciones AS
SELECT id, numero, capacidad, cama, sencilla, camarote, estado
FROM habitaciones
WHERE activo = TRUE;

-- ===========================================================
-- FUNCION: insertar_habitacion()
-- ===========================================================
CREATE OR REPLACE FUNCTION insertar_habitacion(
    p_numero VARCHAR,
    p_tipo VARCHAR,
    p_capacidad INT,
    p_precio_noche NUMERIC,
    p_cama INT,
    p_sencilla INT,
    p_camarote INT
) RETURNS TEXT AS $$
DECLARE
    existe INT;
BEGIN
    SELECT COUNT(*) INTO existe FROM habitaciones WHERE numero = p_numero;

    IF existe > 0 THEN
        RETURN CONCAT('La habitación con número ', p_numero, ' ya existe.');
    ELSE
        INSERT INTO habitaciones (numero, tipo, capacidad, precio_noche, cama, sencilla, camarote)
        VALUES (p_numero, p_tipo, p_capacidad, p_precio_noche, p_cama, p_sencilla, p_camarote);

        RETURN CONCAT('Habitacion ', p_numero, ' insertada correctamente.');
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ===========================================================
-- FIN DEL SCRIPT
-- ===========================================================
