drop database if exists Banco;
create database Banco;

create type estado_cliente as enum ('Activo', 'Inactivo');

create table if not exists clientes(
	id serial primary key,
	identificacion VARCHAR(100) unique not null,
	nombre VARCHAR(100) not null,
	apellido VARCHAR(100) not null,
	direccion VARCHAR(255) not null,
	telefono VARCHAR (15) unique,
	correo VARCHAR(100) unique,
	estado estado_cliente default 'Activo',
	fecha_registro timestamp not null,
	ultima_actividad timestamp 
	);

create type tipo_cuenta as enum ('Corriente', 'Ahorro');
create type estado_cuenta as enum ('Activa', 'Inactiva');

create table if not exists cuentas(
	id serial primary key,
	id_cliente INT,
	tipo tipo_cuenta,
	saldo DECIMAL(15,2),
	limite_saldo DECIMAL(10,2),
	fecha_apertura TIMESTAMP not null,
	estado estado_cuenta default 'Activa',
	foreign key (id_cliente) references clientes(id)
	);

create type tipo_transaccion as enum ('Transferencia', 'Retiro', 'Deposito', 'Pago', 'Inversion');
create type estado_transaccion as enum ('Pendiente', 'Aprobado', 'Completado', 'Rechazado', 'Reembolsado', 'Contracargo', 'Expirado');

create table if not exists transacciones(
	id serial primary key,
	id_cuenta INT,
	tipo tipo_transaccion,
	monto DECIMAL(15,2) not null,
	fecha_transaccion TIMESTAMP,
	referencia VARCHAR(50) not null,
	saldo_anterior DECIMAL(15,2) not null,
	saldo_nuevo DECIMAL(15,2) not null,
	estado estado_transaccion,
	foreign key(id_cuenta) references cuentas(id)
	);

create type prioridad_cheque as enum ('Baja', 'Media', 'Alta');
create type estado_cheque as enum ('No Protestado', 'Protestado', 'Protestado Parcialmente');
create type razon_rechazo_cheque as enum ('Falta de Fondos', 'Cuenta Cancelada', 'Problema de Firma', 'Monto no Coincidente',
										'Cheque Vencido', 'Problema en el Endoso', 'Informacion Faltante', 'Reportado Como Robado');

create table if not exists cheques(
	id serial primary key,
	numero_cheque VARCHAR(20) not null,
	id_cuenta INT,
	beneficiario VARCHAR(100),
	monto DECIMAL(15,2) not null,
	prioridad prioridad_cheque,
	firma_digital VARCHAR(64),
	estado estado_cheque,
	razon_rechazo razon_rechazo_cheque,
	fecha_emision DATE,
	fecha_proceso TIMESTAMP,
	cobrado smallint not null,
	cuenta_saldo_momento DECIMAL(10,2),
	fecha_modificacion TIMESTAMP,
	usuario_modificacion VARCHAR(50),
	foreign key(id_cuenta) references cuentas(id)
)

create table if not exists cheque_secuencial(
	next_val INT
	);