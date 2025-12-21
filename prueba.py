import psycopg2

# Intenta la conexión directa sin tu clase, usando la contraseña simple
try:
    conn = psycopg2.connect(
        host="192.168.1.19", 
        port="5432", 
        user="postgres", 
        password="jhonm320429", 
        database="sistema"
    )
    print("¡Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"[ERROR] Falló la conexión: {e}")