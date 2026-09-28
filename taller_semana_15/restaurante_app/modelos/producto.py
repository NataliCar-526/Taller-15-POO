# Clase que representa un producto del restaurante
class Producto:
    def __init__(self, id_producto: int, nombre: str, precio: float, categoria: str, stock: int):
        self._validar_datos(nombre, precio, categoria, stock)
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    # Valida que los datos del producto sean correctos
    def _validar_datos(self, nombre: str, precio: float, categoria: str, stock: int) -> None:
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        if not categoria or not str(categoria).strip():
            raise ValueError("La categoría no puede estar vacía.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    # Descuenta stock cuando se realiza una venta válida
    def vender(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor a cero.")
        if cantidad > self.stock:
            raise ValueError("Stock insuficiente para realizar la venta.")
        self.stock -= cantidad
        
    # Muestra la información del producto
    def mostrar_informacion(self) -> str:
        return f"Producto: {self.id_producto} | {self.nombre} | {self.categoria} | ${self.precio:.2f} | Stock: {self.stock}"

    # Representación en texto del producto
    def __str__(self) -> str:
        return f"[{self.id_producto}] {self.nombre} - ${self.precio:.2f} ({self.categoria}) - Stock: {self.stock}"

    # Convierte el objeto a diccionario para JSON
    def to_dict(self) -> dict:
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoría": self.categoria,
            "stock": self.stock
        }

    # Crea un objeto Producto desde un diccionario
    @classmethod
    def from_dict(cls, datos: dict):
        return cls(
            id_producto=datos["id_producto"],
            nombre=datos["nombre"],
            precio=datos["precio"],
            categoria=datos["categoría"],
            stock=datos.get("stock", 0)
        )