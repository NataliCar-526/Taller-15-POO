import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from servicios.restaurante_servicio import RestauranteServicio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_ASSETS = os.path.join(BASE_DIR, "assets")

# Vista de acceso (login) simulada del sistema de restaurante
class LoginView(ttk.Frame):
    def __init__(self, contenedor: tk.Tk, servicio: RestauranteServicio, al_iniciar_sesion):
        super().__init__(contenedor, padding=30)
        self.servicio = servicio
        self.al_iniciar_sesion = al_iniciar_sesion
        self._imagen_logo = None  # referencia viva, evita que Tkinter la elimine

        self._construir_widgets()

    def _construir_widgets(self) -> None:
        contenedor_centro = ttk.Frame(self)
        contenedor_centro.pack(expand=True)

        ruta_logo = os.path.join(RUTA_ASSETS, "logo", "logo.png")
        if os.path.exists(ruta_logo):
            imagen = Image.open(ruta_logo)
            imagen.thumbnail((120, 120))
            self._imagen_logo = ImageTk.PhotoImage(imagen)
            ttk.Label(contenedor_centro, image=self._imagen_logo).pack(pady=(0, 10))

        ttk.Label(contenedor_centro, text="Sistema de Restaurante", style="Titulo.TLabel").pack(pady=(0, 2))
        ttk.Label(contenedor_centro, text="Inicio de sesión", foreground="#8a5a44").pack(pady=(0, 20))

        ttk.Label(contenedor_centro, text="Usuario").pack(anchor="w")
        self.entrada_usuario = ttk.Entry(contenedor_centro, width=30)
        self.entrada_usuario.pack(pady=(2, 15))

        ttk.Label(contenedor_centro, text="Contraseña").pack(anchor="w")
        self.entrada_contrasena = ttk.Entry(contenedor_centro, width=30, show="*")
        self.entrada_contrasena.pack(pady=(2, 20))

        ttk.Button(contenedor_centro, text="Ingresar", style="Acento.TButton",
                   command=self._intentar_ingresar).pack(fill="x", pady=5)

        self.etiqueta_mensaje = ttk.Label(contenedor_centro, text="", foreground="#c0392b")
        self.etiqueta_mensaje.pack(pady=10)

    def _intentar_ingresar(self) -> None:
        nombre = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not nombre or not contrasena:
            self.etiqueta_mensaje.config(text="Debe ingresar usuario y contraseña.")
            return

        if self.servicio.validar_acceso(nombre, contrasena):
            self.etiqueta_mensaje.config(text="")
            self.al_iniciar_sesion(nombre)
        else:
            self.etiqueta_mensaje.config(text="Usuario o contraseña incorrectos.")