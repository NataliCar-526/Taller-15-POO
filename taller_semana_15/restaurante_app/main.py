import os
import tkinter as tk
from tkinter import ttk
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "datos")
RUTA_ASSETS = os.path.join(BASE_DIR, "assets")

# Paleta de colores del sistema, basada en el logo
COLOR_FONDO = "#FDF8F2"
COLOR_NARANJA = "#F37901"
COLOR_CAFE_OSCURO = "#33160F"

class Aplicacion:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Sistema de Restaurante")
        self.raiz.geometry("960x600")
        self.raiz.configure(bg=COLOR_FONDO)
        self._configurar_icono_ventana()
        self._configurar_estilos()

        self.archivo_servicio = ArchivoServicio(
            ruta_productos=os.path.join(RUTA_DATOS, "productos.json"),
            ruta_usuarios=os.path.join(RUTA_DATOS, "usuarios.json"),
            ruta_ventas=os.path.join(RUTA_DATOS, "ventas.json")
        )
        self.servicio = RestauranteServicio(self.archivo_servicio)
        self._cargar_datos_iniciales()

        self.vista_actual: tk.Frame | None = None
        self._mostrar_login()

    def _configurar_icono_ventana(self) -> None:
        ruta_icono = os.path.join(RUTA_ASSETS, "logo", "icono.ico")
        if os.path.exists(ruta_icono):
            try:
                self.raiz.iconbitmap(ruta_icono)
            except tk.TclError:
                pass

    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self.raiz)
        estilo.theme_use("clam")

        estilo.configure("TFrame", background=COLOR_FONDO)
        estilo.configure("TLabel", background=COLOR_FONDO, font=("Segoe UI", 10), foreground=COLOR_CAFE_OSCURO)
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 15, "bold"), foreground=COLOR_CAFE_OSCURO, background=COLOR_FONDO)
        estilo.configure("TButton", font=("Segoe UI", 10), padding=6)
        estilo.configure("TEntry", padding=5)
        estilo.configure("TLabelframe", background=COLOR_FONDO, foreground=COLOR_CAFE_OSCURO)
        estilo.configure("TLabelframe.Label", background=COLOR_FONDO, foreground=COLOR_CAFE_OSCURO, font=("Segoe UI", 10, "bold"))

        # Botón de acento (usado para "Ingresar" y otras acciones primarias)
        estilo.configure("Acento.TButton", background=COLOR_NARANJA, foreground="white", font=("Segoe UI", 10, "bold"))
        estilo.map("Acento.TButton", background=[("active", "#D96A00")])
        
        # Estilo de las tablas (Treeview) acorde a la paleta
        estilo.configure("Treeview", background="white", fieldbackground="white",
                         rowheight=26, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", background="#F5E6D3", foreground=COLOR_CAFE_OSCURO,
                         font=("Segoe UI", 10, "bold"))
        estilo.map("Treeview", background=[("selected", COLOR_NARANJA)], foreground=[("selected", "white")])

    def _cargar_datos_iniciales(self) -> None:
        productos = self.archivo_servicio.cargar_productos()
        self.servicio.cargar_productos(productos)
        usuarios = self.archivo_servicio.cargar_usuarios()
        self.servicio.cargar_usuarios(usuarios)
        ventas = self.archivo_servicio.cargar_ventas()
        self.servicio.cargar_ventas(ventas)

    def _limpiar_vista_actual(self) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()

    def _mostrar_login(self) -> None:
        self._limpiar_vista_actual()
        self.vista_actual = LoginView(self.raiz, self.servicio, self._mostrar_main)
        self.vista_actual.pack(fill="both", expand=True)

    def _mostrar_main(self, nombre_usuario: str) -> None:
        self._limpiar_vista_actual()
        self.vista_actual = MainView(self.raiz, self.servicio, nombre_usuario, self._mostrar_login)

def main() -> None:
    raiz = tk.Tk()
    Aplicacion(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()