from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

# Servicio que administra la información del restaurante para la interfaz gráfica
class RestauranteServicio:
    def __init__(self, archivo_servicio: ArchivoServicio):
        self.archivo_servicio = archivo_servicio
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.ventas: list[Venta] = []

    # ===== CARGA DE DATOS =====

    def cargar_productos(self, productos: list[Producto]) -> None:
        self.productos = productos

    def cargar_usuarios(self, usuarios: list[Usuario]) -> None:
        self.usuarios = usuarios

    def cargar_ventas(self, ventas: list[Venta]) -> None:
        self.ventas = ventas

    # ===== ACCESO (LOGIN) =====

    def buscar_usuario_por_nombre(self, nombre: str) -> Usuario | None:
        for usuario in self.usuarios:
            if usuario.nombre == nombre:
                return usuario
        return None

    def validar_acceso(self, nombre: str, contrasena: str) -> bool:
        if not nombre or not contrasena:
            return False
        usuario = self.buscar_usuario_por_nombre(nombre)
        if usuario is None:
            return False
        return usuario.verificar_contrasena(contrasena)

    # ===== CONSULTAS =====

    def listar_productos(self) -> list[Producto]:
        return self.productos

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def listar_ventas(self) -> list[Venta]:
        return self.ventas

    def buscar_producto(self, id_producto: int) -> Producto | None:
        for producto in self.productos:
            if producto.id_producto == id_producto:
                return producto
        return None

    # ===== GESTIÓN DE PRODUCTOS (CRUD) =====

    def agregar_producto(self, id_producto: int, nombre: str, precio: float, categoria: str, stock: int) -> None:
        if self.buscar_producto(id_producto) is not None:
            raise ValueError(f"Ya existe un producto con el ID {id_producto}.")
        nuevo_producto = Producto(id_producto, nombre, precio, categoria, stock)
        self.productos.append(nuevo_producto)
        self._guardar_productos()

    def actualizar_producto(self, id_producto: int, nombre: str, categoria: str, precio: float, stock: int) -> bool:
        producto = self.buscar_producto(id_producto)
        if producto is None:
            return False
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        self._guardar_productos()
        return True

    def eliminar_producto(self, id_producto: int) -> bool:
        producto = self.buscar_producto(id_producto)
        if producto is None:
            return False
        self.productos.remove(producto)
        self._guardar_productos()
        return True

    def _guardar_productos(self) -> None:
        self.archivo_servicio.guardar_productos(self.productos)

    # ===== GESTIÓN DE VENTAS =====

    # Genera el siguiente ID de venta disponible
    def _siguiente_id_venta(self) -> int:
        if not self.ventas:
            return 1
        return max(venta.id_venta for venta in self.ventas) + 1

    # Registra una venta relacionando un usuario existente con un producto existente
    def registrar_venta(self, id_usuario: int, id_producto: int) -> Venta:
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        if usuario is None:
            raise ValueError("Debe seleccionar un usuario válido.")

        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("Debe seleccionar un producto válido.")

        nueva_venta = Venta(self._siguiente_id_venta(), id_usuario, id_producto)
        self.ventas.append(nueva_venta)
        self.archivo_servicio.guardar_ventas(self.ventas)
        return nueva_venta