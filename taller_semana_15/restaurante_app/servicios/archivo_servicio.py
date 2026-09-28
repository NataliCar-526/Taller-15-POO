import json
import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

# Servicio para manejar la persistencia de productos, usuarios y ventas en JSON
class ArchivoServicio:
    def __init__(
        self,
        ruta_productos: str = "datos/productos.json",
        ruta_usuarios: str = "datos/usuarios.json",
        ruta_ventas: str = "datos/ventas.json"
    ):
        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios
        self.ruta_ventas = ruta_ventas
        self._asegurar_directorio(self.ruta_productos)
        self._asegurar_directorio(self.ruta_usuarios)
        self._asegurar_directorio(self.ruta_ventas)

    def _asegurar_directorio(self, ruta_archivo: str) -> None:
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

    def cargar_datos(self, ruta_archivo: str) -> list[dict]:
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            print(f"\n[Info] No se encontró '{ruta_archivo}'. Iniciando base de datos vacía.")
            return []
        except json.JSONDecodeError:
            print(f"\n[Error] El archivo '{ruta_archivo}' contiene un JSON inválido.")
            return []
        except PermissionError:
            print(f"\n[Error] Sin permisos de lectura para '{ruta_archivo}'.")
            return []

    def guardar_datos(self, ruta_archivo: str, datos: list[dict]) -> bool:
        try:
            with open(ruta_archivo, mode='w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"\n[Error] Sin permisos de escritura para '{ruta_archivo}'.")
            return False
        except Exception as e:
            print(f"\n[Error] Error inesperado al guardar: {e}")
            return False

    # ===== PRODUCTOS =====

    def guardar_productos(self, productos: list[Producto]) -> bool:
        datos = [producto.to_dict() for producto in productos]
        return self.guardar_datos(self.ruta_productos, datos)

    def cargar_productos(self) -> list[Producto]:
        datos = self.cargar_datos(self.ruta_productos)
        productos = []
        for item in datos:
            try:
                productos.append(Producto.from_dict(item))
            except (KeyError, ValueError) as e:
                print(f"\n[Advertencia] Registro de producto inválido ignorado: {e}")
        print(f"\n[Info] Productos cargados: {len(productos)}")
        return productos

    # ===== USUARIOS =====

    def guardar_usuarios(self, usuarios: list[Usuario]) -> bool:
        datos = [usuario.to_dict() for usuario in usuarios]
        return self.guardar_datos(self.ruta_usuarios, datos)

    def cargar_usuarios(self) -> list[Usuario]:
        datos = self.cargar_datos(self.ruta_usuarios)
        usuarios = []
        for item in datos:
            try:
                usuarios.append(Usuario.from_dict(item))
            except (KeyError, ValueError) as e:
                print(f"\n[Advertencia] Registro de usuario inválido ignorado: {e}")
        print(f"\n[Info] Usuarios cargados: {len(usuarios)}")
        return usuarios

    # ===== VENTAS =====

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        datos = [venta.to_dict() for venta in ventas]
        return self.guardar_datos(self.ruta_ventas, datos)

    def cargar_ventas(self) -> list[Venta]:
        datos = self.cargar_datos(self.ruta_ventas)
        ventas = []
        for item in datos:
            try:
                ventas.append(Venta.from_dict(item))
            except (KeyError, ValueError) as e:
                print(f"\n[Advertencia] Registro de venta inválido ignorado: {e}")
        print(f"\n[Info] Ventas cargadas: {len(ventas)}")
        return ventas