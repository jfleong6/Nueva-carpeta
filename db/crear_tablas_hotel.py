import psycopg2

def crear_tablas_hotel():
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="tu_password",
        database="hotel_db"
    )
    cursor = conn.cursor()

    # ==== HABITACIONES ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habitaciones (
            id SERIAL PRIMARY KEY,
            numero VARCHAR(10) UNIQUE,
            tipo VARCHAR(50),
            capacidad INT,
            precio_noche NUMERIC(10,2),
            cama BOOLEAN DEFAULT FALSE,
            sencilla BOOLEAN DEFAULT FALSE,
            camarote BOOLEAN DEFAULT FALSE,
            estado VARCHAR(10) DEFAULT '1', -- 1 libre, 2 ocupada, 3 reservada
            activo BOOLEAN DEFAULT TRUE
        );
    """)

    # ==== GRUPOS HOTEL ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grupos_hotel (
            id SERIAL PRIMARY KEY,
            nombre_grupo VARCHAR(100),
            tipo_cuenta VARCHAR(20) CHECK (tipo_cuenta IN ('grupal', 'individual'))
        );
    """)

    # ==== RESERVAS ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas_hotel (
            id SERIAL PRIMARY KEY,
            cliente_id INT,
            habitacion_id INT,
            grupo_id INT,
            fecha_entrada DATE,
            fecha_salida DATE,
            estado VARCHAR(15) CHECK (estado IN ('reservada', 'confirmada', 'cancelada')) DEFAULT 'reservada',
            total NUMERIC(12,2),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id),
            FOREIGN KEY (grupo_id) REFERENCES grupos_hotel(id)
        );
    """)

    # ==== REGISTRO HUESPED ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro_huesped (
            id SERIAL PRIMARY KEY,
            reserva_id INT REFERENCES reservas_hotel(id),
            nombre_completo VARCHAR(100),
            tipo_documento VARCHAR(10),
            numero_documento VARCHAR(20),
            nacionalidad VARCHAR(50),
            fecha_nacimiento DATE,
            sexo VARCHAR(10),
            telefono VARCHAR(20),
            email VARCHAR(80),
            fecha_ingreso DATE,
            fecha_salida DATE,
            es_principal BOOLEAN DEFAULT FALSE,
            observaciones TEXT
        );
    """)

    # ==== CONSUMOS ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumos_hotel (
            id SERIAL PRIMARY KEY,
            reserva_id INT REFERENCES reservas_hotel(id),
            producto_id INT,
            cantidad INT,
            precio_unitario NUMERIC(10,2),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # ==== VENTAS ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas_hotel (
            id SERIAL PRIMARY KEY,
            reserva_id INT REFERENCES reservas_hotel(id),
            cliente_id INT REFERENCES clientes(id),
            usuario_id INT REFERENCES usuarios(id),
            total NUMERIC(12,2),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado VARCHAR(20) DEFAULT 'completada'
        );
    """)

    # ==== DETALLE VENTAS ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta_hotel (
            id SERIAL PRIMARY KEY,
            venta_id INT REFERENCES ventas_hotel(id),
            producto_id INT,
            cantidad INT,
            precio_unitario NUMERIC(10,2)
        );
    """)

    # ==== PAGOS ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos_hotel (
            id SERIAL PRIMARY KEY,
            venta_id INT REFERENCES ventas_hotel(id),
            tipo_pago_id INT REFERENCES tipos_pagos(id),
            monto NUMERIC(12,2),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # ==== MOVIMIENTOS INVENTARIO ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos_inventario_hotel (
            id SERIAL PRIMARY KEY,
            producto_id INT,
            tipo VARCHAR(10) CHECK (tipo IN ('entrada', 'salida', 'traslado')),
            cantidad INT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            referencia TEXT
        );
    """)

    # ==== SERVICIOS COMBO ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios_combo (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(80) NOT NULL,
            descripcion TEXT,
            precio NUMERIC(10,2) NOT NULL,
            es_por_persona BOOLEAN DEFAULT TRUE
        );
    """)

    # ==== DETALLE COMBO ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios_combo_detalle (
            id SERIAL PRIMARY KEY,
            combo_id INT REFERENCES servicios_combo(id) ON DELETE CASCADE,
            beneficio TEXT NOT NULL,
            orden INT DEFAULT 1
        );
    """)

    # ==== COMBOS ASIGNADOS ====
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios_combo_asignado (
            id SERIAL PRIMARY KEY,
            registro_huesped_id INT REFERENCES registro_huesped(id),
            combo_id INT REFERENCES servicios_combo(id),
            cantidad_personas INT DEFAULT 1,
            precio_total NUMERIC(10,2) NOT NULL
        );
    """)

    # ==== VISTA HABITACIONES ====
    cursor.execute("""
        CREATE OR REPLACE VIEW cargar_habitaciones AS
        SELECT id, numero, capacidad, cama, sencilla, camarote, estado
        FROM habitaciones
        WHERE activo = TRUE;
    """)

    # ==== FUNCIÓN INSERTAR HABITACIÓN ====
    cursor.execute("""
        CREATE OR REPLACE FUNCTION insertar_habitacion(
            p_numero TEXT,
            p_tipo TEXT,
            p_capacidad INT,
            p_precio_noche NUMERIC,
            p_cama BOOLEAN DEFAULT FALSE,
            p_sencilla BOOLEAN DEFAULT FALSE,
            p_camarote BOOLEAN DEFAULT FALSE,
            p_estado TEXT DEFAULT '1',
            p_activo BOOLEAN DEFAULT TRUE
        )
        RETURNS TEXT AS $$
        DECLARE
            existe INT;
        BEGIN
            SELECT COUNT(*) INTO existe FROM habitaciones WHERE numero = p_numero;
            IF existe > 0 THEN
                RETURN '⚠️ La habitación ' || p_numero || ' ya existe.';
            END IF;

            INSERT INTO habitaciones (
                numero, tipo, capacidad, precio_noche, cama, sencilla, camarote, estado, activo
            ) VALUES (
                p_numero, p_tipo, p_capacidad, p_precio_noche, p_cama, p_sencilla, p_camarote, p_estado, p_activo
            );

            RETURN '✅ Habitación ' || p_numero || ' insertada correctamente.';
        END;
        $$ LANGUAGE plpgsql;
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas y funciones del módulo Hotel creadas correctamente en PostgreSQL.")
