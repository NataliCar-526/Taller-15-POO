# Clase que representa un usuario del restaurante
class Usuario:
    def __init__(self, id_usuario: int, nombre: str, correo: str, contrasena: str):
        self._validar_datos(nombre, correo, contrasena)
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    # Valida que los datos del usuario sean correctos
    def _validar_datos(self, nombre: str, correo: str, contrasena: str) -> None:
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo or "@" not in correo:
            raise ValueError("El correo del usuario no es válido.")
        if not contrasena or not str(contrasena).strip():
            raise ValueError("La contraseña del usuario no puede estar vacía.")

    # Verifica si la contraseña ingresada coincide con la del usuario
    def verificar_contrasena(self, contrasena: str) -> bool:
        return self.contrasena == contrasena

    # Muestra la información del usuario
    def mostrar_informacion(self) -> str:
        return f"Usuario: {self.id_usuario} | {self.nombre} | {self.correo}"

    # Representación en texto del usuario
    def __str__(self) -> str:
        return f"[{self.id_usuario}] {self.nombre} ({self.correo})"

    # Convierte el objeto a diccionario para JSON
    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "correo": self.correo,
            "contraseña": self.contrasena
        }

    # Crea un objeto Usuario desde un diccionario
    @classmethod
    def from_dict(cls, datos: dict):
        return cls(
            id_usuario=datos["id_usuario"],
            nombre=datos["nombre"],
            correo=datos["correo"],
            contrasena=datos["contraseña"]
        )