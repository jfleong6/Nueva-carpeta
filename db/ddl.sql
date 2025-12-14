-- DROP SCHEMA core;

CREATE SCHEMA core AUTHORIZATION postgres;

-- DROP SEQUENCE core.clientes_id_seq;

CREATE SEQUENCE core.clientes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE core.clientes_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE core.clientes_id_seq TO postgres;

-- DROP SEQUENCE core.tipos_pagos_id_seq;

CREATE SEQUENCE core.tipos_pagos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE core.tipos_pagos_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE core.tipos_pagos_id_seq TO postgres;

-- DROP SEQUENCE core.usuarios_id_seq;

CREATE SEQUENCE core.usuarios_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE core.usuarios_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE core.usuarios_id_seq TO postgres;
-- core.clientes definition

-- Drop table

-- DROP TABLE core.clientes;

CREATE TABLE core.clientes (
	id serial4 NOT NULL,
	nombre_completo text NOT NULL,
	tipo_documento text NULL,
	numero_documento text NULL,
	fecha_nacimiento date NULL,
	sexo text NULL,
	telefono text NULL,
	email text NULL,
	direccion text NULL,
	ciudad text NULL,
	departamento text NULL,
	pais text NULL,
	notas text NULL,
	fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT clientes_numero_documento_key UNIQUE (numero_documento),
	CONSTRAINT clientes_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE core.clientes OWNER TO postgres;
GRANT ALL ON TABLE core.clientes TO postgres;


-- core.tipos_pagos definition

-- Drop table

-- DROP TABLE core.tipos_pagos;

CREATE TABLE core.tipos_pagos (
	id serial4 NOT NULL,
	nombre text NOT NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT tipos_pagos_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE core.tipos_pagos OWNER TO postgres;
GRANT ALL ON TABLE core.tipos_pagos TO postgres;


-- core.usuarios definition

-- Drop table

-- DROP TABLE core.usuarios;

CREATE TABLE core.usuarios (
	id serial4 NOT NULL,
	nombre text NOT NULL,
	email text NOT NULL,
	rol text NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT usuarios_email_key UNIQUE (email),
	CONSTRAINT usuarios_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE core.usuarios OWNER TO postgres;
GRANT ALL ON TABLE core.usuarios TO postgres;




-- Permissions

GRANT ALL ON SCHEMA core TO postgres;

-- DROP SCHEMA hotel;

CREATE SCHEMA hotel AUTHORIZATION postgres;

-- DROP SEQUENCE hotel.consumos_hotel_id_seq;

CREATE SEQUENCE hotel.consumos_hotel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.consumos_hotel_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.consumos_hotel_id_seq TO postgres;

-- DROP SEQUENCE hotel.detalle_venta_hotel_id_seq;

CREATE SEQUENCE hotel.detalle_venta_hotel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.detalle_venta_hotel_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.detalle_venta_hotel_id_seq TO postgres;

-- DROP SEQUENCE hotel.grupos_hotel_id_seq;

CREATE SEQUENCE hotel.grupos_hotel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.grupos_hotel_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.grupos_hotel_id_seq TO postgres;

-- DROP SEQUENCE hotel.habitaciones_id_seq;

CREATE SEQUENCE hotel.habitaciones_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.habitaciones_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.habitaciones_id_seq TO postgres;

-- DROP SEQUENCE hotel.movimientos_inventario_hotel_id_seq;

CREATE SEQUENCE hotel.movimientos_inventario_hotel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.movimientos_inventario_hotel_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.movimientos_inventario_hotel_id_seq TO postgres;

-- DROP SEQUENCE hotel.pagos_hotel_id_seq;

CREATE SEQUENCE hotel.pagos_hotel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.pagos_hotel_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.pagos_hotel_id_seq TO postgres;

-- DROP SEQUENCE hotel.registro_huesped_id_seq;

CREATE SEQUENCE hotel.registro_huesped_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.registro_huesped_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.registro_huesped_id_seq TO postgres;

-- DROP SEQUENCE hotel.reservas_hotel_id_seq;

CREATE SEQUENCE hotel.reservas_hotel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.reservas_hotel_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.reservas_hotel_id_seq TO postgres;

-- DROP SEQUENCE hotel.servicios_combo_asignado_id_seq;

CREATE SEQUENCE hotel.servicios_combo_asignado_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.servicios_combo_asignado_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.servicios_combo_asignado_id_seq TO postgres;

-- DROP SEQUENCE hotel.servicios_combo_detalle_id_seq;

CREATE SEQUENCE hotel.servicios_combo_detalle_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.servicios_combo_detalle_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.servicios_combo_detalle_id_seq TO postgres;

-- DROP SEQUENCE hotel.servicios_combo_id_seq;

CREATE SEQUENCE hotel.servicios_combo_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.servicios_combo_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.servicios_combo_id_seq TO postgres;

-- DROP SEQUENCE hotel.ventas_hotel_id_seq;

CREATE SEQUENCE hotel.ventas_hotel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE hotel.ventas_hotel_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE hotel.ventas_hotel_id_seq TO postgres;
-- hotel.grupos_hotel definition

-- Drop table

-- DROP TABLE hotel.grupos_hotel;

CREATE TABLE hotel.grupos_hotel (
	id serial4 NOT NULL,
	nombre_grupo varchar(100) NULL,
	tipo_cuenta varchar(20) NOT NULL,
	CONSTRAINT grupos_hotel_pkey PRIMARY KEY (id),
	CONSTRAINT grupos_hotel_tipo_cuenta_check CHECK (((tipo_cuenta)::text = ANY ((ARRAY['grupal'::character varying, 'individual'::character varying])::text[])))
);

-- Permissions

ALTER TABLE hotel.grupos_hotel OWNER TO postgres;
GRANT ALL ON TABLE hotel.grupos_hotel TO postgres;


-- hotel.habitaciones definition

-- Drop table

-- DROP TABLE hotel.habitaciones;

CREATE TABLE hotel.habitaciones (
	id serial4 NOT NULL,
	numero varchar(20) NULL,
	tipo varchar(50) NULL,
	capacidad int4 NULL,
	precio_noche numeric(10, 2) NULL,
	cama int2 DEFAULT 0 NULL,
	sencilla int2 DEFAULT 0 NULL,
	camarote int2 DEFAULT 0 NULL,
	estado varchar(10) DEFAULT '1'::character varying NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT habitaciones_numero_key UNIQUE (numero),
	CONSTRAINT habitaciones_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE hotel.habitaciones OWNER TO postgres;
GRANT ALL ON TABLE hotel.habitaciones TO postgres;


-- hotel.hoel definition

-- Drop table

-- DROP TABLE hotel.hoel;

CREATE TABLE hotel.hoel (

);

-- Permissions

ALTER TABLE hotel.hoel OWNER TO postgres;
GRANT ALL ON TABLE hotel.hoel TO postgres;


-- hotel.movimientos_inventario_hotel definition

-- Drop table

-- DROP TABLE hotel.movimientos_inventario_hotel;

CREATE TABLE hotel.movimientos_inventario_hotel (
	id serial4 NOT NULL,
	producto_id int4 NULL,
	tipo varchar(10) NULL,
	cantidad int4 NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	referencia varchar(100) NULL,
	CONSTRAINT movimientos_inventario_hotel_pkey PRIMARY KEY (id),
	CONSTRAINT movimientos_inventario_hotel_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['entrada'::character varying, 'salida'::character varying, 'traslado'::character varying])::text[])))
);

-- Permissions

ALTER TABLE hotel.movimientos_inventario_hotel OWNER TO postgres;
GRANT ALL ON TABLE hotel.movimientos_inventario_hotel TO postgres;


-- hotel.servicios_combo definition

-- Drop table

-- DROP TABLE hotel.servicios_combo;

CREATE TABLE hotel.servicios_combo (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	descripcion text NULL,
	precio numeric(10, 2) NOT NULL,
	es_por_persona bool DEFAULT true NULL,
	CONSTRAINT servicios_combo_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE hotel.servicios_combo OWNER TO postgres;
GRANT ALL ON TABLE hotel.servicios_combo TO postgres;


-- hotel.reservas_hotel definition

-- Drop table

-- DROP TABLE hotel.reservas_hotel;

CREATE TABLE hotel.reservas_hotel (
	id serial4 NOT NULL,
	cliente_id int4 NULL,
	habitacion_id int4 NULL,
	grupo_id int4 NULL,
	fecha_entrada timestamp NULL,
	fecha_salida timestamp NULL,
	estado varchar(20) DEFAULT 'reservada'::character varying NULL,
	total numeric(10, 2) NULL,
	CONSTRAINT reservas_hotel_estado_check CHECK (((estado)::text = ANY ((ARRAY['reservada'::character varying, 'confirmada'::character varying, 'cancelada'::character varying])::text[]))),
	CONSTRAINT reservas_hotel_pkey PRIMARY KEY (id),
	CONSTRAINT reservas_hotel_grupo_id_fkey FOREIGN KEY (grupo_id) REFERENCES hotel.grupos_hotel(id),
	CONSTRAINT reservas_hotel_habitacion_id_fkey FOREIGN KEY (habitacion_id) REFERENCES hotel.habitaciones(id)
);

-- Permissions

ALTER TABLE hotel.reservas_hotel OWNER TO postgres;
GRANT ALL ON TABLE hotel.reservas_hotel TO postgres;


-- hotel.servicios_combo_detalle definition

-- Drop table

-- DROP TABLE hotel.servicios_combo_detalle;

CREATE TABLE hotel.servicios_combo_detalle (
	id serial4 NOT NULL,
	combo_id int4 NOT NULL,
	beneficio text NOT NULL,
	orden int4 DEFAULT 1 NULL,
	CONSTRAINT servicios_combo_detalle_pkey PRIMARY KEY (id),
	CONSTRAINT servicios_combo_detalle_combo_id_fkey FOREIGN KEY (combo_id) REFERENCES hotel.servicios_combo(id) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE hotel.servicios_combo_detalle OWNER TO postgres;
GRANT ALL ON TABLE hotel.servicios_combo_detalle TO postgres;


-- hotel.ventas_hotel definition

-- Drop table

-- DROP TABLE hotel.ventas_hotel;

CREATE TABLE hotel.ventas_hotel (
	id serial4 NOT NULL,
	reserva_id int4 NULL,
	cliente_id int4 NULL,
	usuario_id int4 NULL,
	total numeric(10, 2) NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	estado varchar(30) DEFAULT 'completada'::character varying NULL,
	CONSTRAINT ventas_hotel_pkey PRIMARY KEY (id),
	CONSTRAINT ventas_hotel_reserva_id_fkey FOREIGN KEY (reserva_id) REFERENCES hotel.reservas_hotel(id)
);

-- Permissions

ALTER TABLE hotel.ventas_hotel OWNER TO postgres;
GRANT ALL ON TABLE hotel.ventas_hotel TO postgres;


-- hotel.consumos_hotel definition

-- Drop table

-- DROP TABLE hotel.consumos_hotel;

CREATE TABLE hotel.consumos_hotel (
	id serial4 NOT NULL,
	reserva_id int4 NULL,
	producto_id int4 NULL,
	cantidad int4 NULL,
	precio_unitario numeric(10, 2) NULL,
	fecha timestamp NULL,
	CONSTRAINT consumos_hotel_pkey PRIMARY KEY (id),
	CONSTRAINT consumos_hotel_reserva_id_fkey FOREIGN KEY (reserva_id) REFERENCES hotel.reservas_hotel(id)
);

-- Permissions

ALTER TABLE hotel.consumos_hotel OWNER TO postgres;
GRANT ALL ON TABLE hotel.consumos_hotel TO postgres;


-- hotel.detalle_venta_hotel definition

-- Drop table

-- DROP TABLE hotel.detalle_venta_hotel;

CREATE TABLE hotel.detalle_venta_hotel (
	id serial4 NOT NULL,
	venta_id int4 NULL,
	producto_id int4 NULL,
	cantidad int4 NULL,
	precio_unitario numeric(10, 2) NULL,
	CONSTRAINT detalle_venta_hotel_pkey PRIMARY KEY (id),
	CONSTRAINT detalle_venta_hotel_venta_id_fkey FOREIGN KEY (venta_id) REFERENCES hotel.ventas_hotel(id)
);

-- Permissions

ALTER TABLE hotel.detalle_venta_hotel OWNER TO postgres;
GRANT ALL ON TABLE hotel.detalle_venta_hotel TO postgres;


-- hotel.pagos_hotel definition

-- Drop table

-- DROP TABLE hotel.pagos_hotel;

CREATE TABLE hotel.pagos_hotel (
	id serial4 NOT NULL,
	venta_id int4 NULL,
	tipo_pago_id int4 NULL,
	monto numeric(10, 2) NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT pagos_hotel_pkey PRIMARY KEY (id),
	CONSTRAINT pagos_hotel_venta_id_fkey FOREIGN KEY (venta_id) REFERENCES hotel.ventas_hotel(id)
);

-- Permissions

ALTER TABLE hotel.pagos_hotel OWNER TO postgres;
GRANT ALL ON TABLE hotel.pagos_hotel TO postgres;


-- hotel.registro_huesped definition

-- Drop table

-- DROP TABLE hotel.registro_huesped;

CREATE TABLE hotel.registro_huesped (
	id serial4 NOT NULL,
	reserva_id int4 NULL,
	nombre_completo varchar(100) NULL,
	tipo_documento varchar(20) NULL,
	numero_documento varchar(30) NULL,
	nacionalidad varchar(50) NULL,
	fecha_nacimiento date NULL,
	sexo varchar(10) NULL,
	telefono varchar(20) NULL,
	email varchar(100) NULL,
	fecha_ingreso timestamp NULL,
	fecha_salida timestamp NULL,
	es_principal bool DEFAULT false NULL,
	observaciones text NULL,
	CONSTRAINT registro_huesped_pkey PRIMARY KEY (id),
	CONSTRAINT registro_huesped_reserva_id_fkey FOREIGN KEY (reserva_id) REFERENCES hotel.reservas_hotel(id)
);

-- Permissions

ALTER TABLE hotel.registro_huesped OWNER TO postgres;
GRANT ALL ON TABLE hotel.registro_huesped TO postgres;


-- hotel.servicios_combo_asignado definition

-- Drop table

-- DROP TABLE hotel.servicios_combo_asignado;

CREATE TABLE hotel.servicios_combo_asignado (
	id serial4 NOT NULL,
	registro_huesped_id int4 NOT NULL,
	combo_id int4 NOT NULL,
	cantidad_personas int4 DEFAULT 1 NULL,
	precio_total numeric(10, 2) NOT NULL,
	CONSTRAINT servicios_combo_asignado_pkey PRIMARY KEY (id),
	CONSTRAINT servicios_combo_asignado_combo_id_fkey FOREIGN KEY (combo_id) REFERENCES hotel.servicios_combo(id),
	CONSTRAINT servicios_combo_asignado_registro_huesped_id_fkey FOREIGN KEY (registro_huesped_id) REFERENCES hotel.registro_huesped(id)
);

-- Permissions

ALTER TABLE hotel.servicios_combo_asignado OWNER TO postgres;
GRANT ALL ON TABLE hotel.servicios_combo_asignado TO postgres;



-- DROP FUNCTION hotel.insertar_habitacion(text, text, int4, float4, int4, int4, int4, text, bool);

CREATE OR REPLACE FUNCTION hotel.insertar_habitacion(p_numero text, p_tipo text, p_capacidad integer, p_precio_noche real, p_cama integer DEFAULT 0, p_sencilla integer DEFAULT 0, p_camarote integer DEFAULT 0, p_estado text DEFAULT '1'::text, p_activo boolean DEFAULT true)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Tu lógica aquí...
END;
$function$
;

-- Permissions

ALTER FUNCTION hotel.insertar_habitacion(text, text, int4, float4, int4, int4, int4, text, bool) OWNER TO postgres;
GRANT ALL ON FUNCTION hotel.insertar_habitacion(text, text, int4, float4, int4, int4, int4, text, bool) TO postgres;


-- Permissions

GRANT ALL ON SCHEMA hotel TO postgres;