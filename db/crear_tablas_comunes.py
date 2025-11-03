import sqlite3

def crear_tablas_comunes():
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT UNIQUE,
        rol TEXT,
        activo BOOLEAN DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT,
        tipo_documento TEXT,
        numero_documento TEXT UNIQUE,
        fecha_nacimiento TEXT,
        sexo TEXT,
        telefono TEXT,
        email TEXT,
        direccion TEXT,
        ciudad TEXT,
        departamento TEXT,
        pais TEXT,
        notas TEXT,
        fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
        activo BOOLEAN DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipos_pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        activo BOOLEAN DEFAULT 1
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas comunes creadas correctamente.")

if __name__ == "__main__":
    crear_tablas_comunes()
