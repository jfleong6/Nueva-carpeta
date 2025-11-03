from db.conexion_base import ConexionBase
conn = ConexionBase(db_name = "hotel.db")

class Habitacion:
    def __init__(self, id, numero, capacidad, cama, camarote):
        self.id = id
        self.numero = numero
        self.capacidad = capacidad
        self.cama = cama
        self.camarote = camarote
        self.imprimir()
    def imprimir(self):
        print(self.__dict__)

def obtener_habitaciones():
    query = """
    SELECT h.id, h.numero, h.capacidad, h.cama, h.camarote
    FROM habitaciones h
    """
    filas = conn.consultar(query)
    return [Habitacion(*fila) for fila in filas]

if __name__ == "__main__":
    obtener_habitaciones()