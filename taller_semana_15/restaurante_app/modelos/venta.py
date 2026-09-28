from datetime import date

# Clase que representa la venta de un producto a un usuario
class Venta:
    def __init__(self, id_venta: int, id_usuario: int, id_producto: int, fecha: str | None = None):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.id_producto = id_producto
        self.fecha = fecha if fecha else date.today().isoformat()

    # Muestra la información de la venta
    def mostrar_informacion(self) -> str:
        return f"Venta {self.id_venta} -> Usuario: {self.id_usuario} | Producto: {self.id_producto} | Fecha: {self.fecha}"

    # Representación en texto de la venta
    def __str__(self) -> str:
        return f"Venta {self.id_venta}: usuario {self.id_usuario}, producto {self.id_producto} ({self.fecha})"

    # Convierte el objeto a diccionario para JSON
    def to_dict(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "id_usuario": self.id_usuario,
            "id_producto": self.id_producto,
            "fecha": self.fecha
        }

    # Crea un objeto Venta desde un diccionario
    @classmethod
    def from_dict(cls, datos: dict):
        return cls(
            id_venta=datos["id_venta"],
            id_usuario=datos["id_usuario"],
            id_producto=datos["id_producto"],
            fecha=datos.get("fecha")
        )