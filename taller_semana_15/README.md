# Tarea Semana 15 - Manejo de eventos en restaurante_app

**Estudiante:** NATALIA BELÉN CARVAJAL DÍAZ

---

## Descripción del sistema

Esta semana *restaurante_app* incorpora una nueva sección de **Ventas** para trabajar los fundamentos del **manejo de eventos** en Tkinter. Una acción del usuario (presionar el botón "Registrar venta") inicia una respuesta en la aplicación: el botón ejecuta un callback mediante `command=`, el callback delega la operación a `RestauranteServicio`, la venta se guarda en `ventas.json` y la interfaz se actualiza mostrando el resultado.

Además, se mantiene todo lo desarrollado en semanas anteriores (inicio de sesión, consulta de usuarios y gestión completa de productos) y se rediseña la interfaz para mejorar su organización y consistencia visual.

---

## Evolución respecto a la Semana 14

| Aspecto | Semana 14 | Semana 15 |
|---------|-----------|-----------|
| Secciones | Usuarios y Productos | Inicio, Usuarios, Productos y **Ventas** |
| Navegación | Botones horizontales en la parte superior | **Sidebar lateral** con íconos y resaltado de la sección activa |
| Distribución | Formulario arriba y tabla debajo | Formulario a la izquierda y tabla a la derecha, agrupados en `LabelFrame` |
| Recursos visuales | Sin recursos externos | Carpeta `assets/` con logo, ícono de ventana e íconos de botones |
| Paleta de colores | Colores genéricos | Colores tomados del logo (naranja, crema y café) |
| Persistencia | `productos.json` y `usuarios.json` | Se agrega `ventas.json` |
| Usuarios | Lista simple | Tabla `Treeview`, coherente con las demás secciones |
| Información general | No existía | Barra de estado con totales de productos, usuarios y ventas |

---

## Estructura del proyecto

```
restaurante_app/
├── assets/
│ ├── logo/
│ │ ├── logo.png           # Logo del sistema
│ │ └── icono.ico          # Ícono de la ventana
│ └── icons/
│ ├── home.png
│ ├── usuarios.png
│ ├── productos.png
│ ├── ventas.png
│ ├── logout.png
│ ├── agregar.png
│ ├── buscar.png
│ ├── editar.png
│ ├── eliminar.png
│ └── limpiar.png
├── datos/
│ ├── productos.json
│ ├── usuarios.json
│ └── ventas.json          # Nuevo: persistencia de ventas
├── modelos/
│ ├── init.py
│ ├── producto.py
│ ├── usuario.py
│ └── venta.py             # Nuevo: relaciona usuario, producto y fecha
├── servicios/
│ ├── init.py
│ ├── archivo_servicio.py        # Incorpora carga y guardado de ventas
│ └── restaurante_servicio.py    # Incorpora el registro y la consulta de ventas
├── ui/
│ ├── init.py
│ ├── login_view.py        # Ahora muestra el logo
│ └── main_view.py         # Sidebar, nueva sección de ventas y logo en Inicio
└── main.py
```

En la raíz del repositorio se encuentra `README.md`.

---

## Responsabilidad de cada componente

| Componente | Responsabilidad |
|------------|-----------------|
| Producto | Representa un producto del restaurante (id, nombre, precio, categoría, stock) |
| Usuario | Representa un usuario del sistema, con contraseña para el acceso simulado |
| Venta | Representa la relación entre un usuario, un producto y la fecha de la operación |
| ArchivoServicio | Lee y escribe productos, usuarios y ventas en sus archivos JSON |
| RestauranteServicio | Concentra la lógica de negocio: login, CRUD de productos y registro de ventas, con validaciones y persistencia |
| LoginView | Pantalla de acceso con el logo del sistema |
| MainView | Panel principal con sidebar, secciones (Inicio, Usuarios, Productos, Ventas) y barra de estado |
| main.py | Crea la ventana, aplica el estilo general, carga los datos y controla el cambio entre vistas |

---

## Gestión de ventas

**Modelo Venta:** cada venta guarda un identificador propio (`id_venta`), el usuario (`id_usuario`), el producto (`id_producto`) y la `fecha` en que se registró.

**Sección Ventas:** contiene un formulario con dos listas desplegables (`ttk.Combobox`) para seleccionar un usuario y un producto ya registrados, un botón "Registrar venta" y una tabla (`ttk.Treeview`) con las ventas registradas. En la tabla se muestran los nombres del usuario y del producto en lugar de sus identificadores.

**Validaciones:** las realiza `RestauranteServicio.registrar_venta()`, que comprueba que el usuario y el producto seleccionados existan antes de crear la venta. La vista solo verifica que ambas listas tengan una selección y muestra el mensaje que devuelve el servicio.

En esta versión la venta relaciona usuario, producto y fecha de forma sencilla, tal como pide la actividad. No incluye cantidades ni descuento de stock.

---

## Manejo de eventos: command= y callbacks

El botón "Registrar venta" se asocia al callback sin paréntesis, es decir, se le entrega la referencia al método y no su resultado:

```python
self._boton_accion(formulario, "Registrar venta", "ventas", COLOR_NARANJA,
                   COLOR_NARANJA_HOVER, self._callback_registrar_venta)
```

Cuando el usuario presiona el botón, Tkinter ejecuta `_callback_registrar_venta()`, que sigue este flujo:

---

```
USUARIO
↓
presiona "Registrar venta"
↓
BOTÓN
↓
command=self._callback_registrar_venta
↓
CALLBACK
├─ lee los valores seleccionados en los Combobox
├─ traduce los nombres a identificadores
└─ llama a RestauranteServicio.registrar_venta(...)
↓
RestauranteServicio valida y crea la Venta
↓
ArchivoServicio guarda ventas.json
↓
La tabla y la barra de estado se actualizan y se muestra el mensaje de resultado
```

---

El callback obtiene datos de la interfaz y coordina la operación, pero no contiene reglas del restaurante ni escribe archivos: eso corresponde al servicio.

Los demás botones del sistema (Registrar, Cargar por ID, Actualizar, Eliminar, Limpiar, Cerrar sesión y la navegación del sidebar) siguen el mismo patrón con `command=`.

---

## Persistencia

`RestauranteServicio` recibe una instancia de `ArchivoServicio` y la utiliza para guardar automáticamente después de cada operación que modifica datos:

| Operación | Archivo actualizado |
|-----------|---------------------|
| Registrar, actualizar o eliminar producto | `productos.json` |
| Registrar venta | `ventas.json` |

Al iniciar la aplicación, `main.py` carga productos, usuarios y ventas desde sus archivos JSON y los entrega al servicio. Las ventas registradas se recuperan al cerrar y volver a ejecutar la aplicación. Las vistas nunca leen ni escriben archivos JSON directamente.

---

## Interfaz y recursos visuales

- **Carpeta `assets/`:** contiene el logo, el ícono de la ventana y los íconos de la navegación y de los botones de acción.
- **Logo:** aparece en la pantalla de acceso, en el sidebar y en la pantalla de Inicio, que es la primera que se muestra al ingresar.
- **Sidebar:** botones con ícono; la sección activa se resalta en naranja y "Cerrar sesión" queda al final.
- **Formularios y tablas:** cada bloque se agrupa en un `LabelFrame` con título; el formulario va a la izquierda y la tabla a la derecha.
- **Botones de acción:** cada uno tiene ícono y color según su función (registrar, cargar, actualizar, eliminar y limpiar).
- **Paleta:** naranja, crema y café, tomados del logo del sistema.
- **Barra de estado:** muestra el total de productos, usuarios y ventas y se actualiza después de cada operación.

---

## Excepciones controladas

| Excepción | ¿Cuándo ocurre? | ¿Cómo se maneja? |
|-----------|-----------------|------------------|
| FileNotFoundError | El archivo JSON no existe | Se inicia esa colección vacía |
| JSONDecodeError | El archivo JSON tiene contenido inválido | Se inicia esa colección vacía |
| PermissionError | No hay permisos de lectura o escritura | Se muestra un mensaje de error |
| KeyError | Un registro no tiene una clave esperada | Se omite el registro dañado |
| ValueError | Datos inválidos, ID duplicado o venta con usuario o producto inexistente | Se muestra el mensaje en la interfaz sin interrumpir la aplicación |
| TclError | El sistema no admite el archivo `.ico` como ícono de ventana | Se ignora y la aplicación continúa con el ícono predeterminado |

---

## Pruebas realizadas

1. Se ejecutó `main.py` y la aplicación inició sin errores mostrando primero la pantalla de acceso con el logo.
2. Se comprobó que el inicio de sesión sigue funcionando, con mensajes ante campos vacíos y credenciales incorrectas.
3. Se verificó que al ingresar se muestra la pantalla de Inicio con el logo.
4. Se comprobó que las secciones Usuarios y Productos mantienen las funciones desarrolladas anteriormente (consulta, registro, carga por ID, actualización y eliminación).
5. Se verificó que existe la sección Ventas y que permite seleccionar un usuario y un producto registrados.
6. Se registró una venta con el botón "Registrar venta" y apareció en la tabla de ventas con la fecha correspondiente.
7. Se comprobó que la venta se guardó en `ventas.json`.
8. Se intentó registrar una venta sin seleccionar usuario o producto y se mostró el mensaje de aviso.
9. Se cerró y volvió a ejecutar la aplicación y las ventas registradas se recuperaron correctamente.

---

## Instrucciones de ejecución

1. Instalar la dependencia necesaria (Pillow, utilizada para mostrar el logo y los íconos): `pip install -r requirements.txt`
2. Ubicarse dentro de la carpeta `restaurante_app/`.
3. Ejecutar: `python main.py`
4. Ingresar un usuario y contraseña registrados en `datos/usuarios.json`.
5. Navegar con el menú lateral: Inicio, Usuarios, Productos y Ventas.
6. Para registrar una venta, ir a **Ventas**, seleccionar un usuario y un producto y presionar "Registrar venta".

---

## Reflexión

Esta semana permitió comprender cómo una acción del usuario se convierte en una respuesta de la aplicación: el botón no ejecuta la operación por sí mismo, sino que la delega a un callback mediante `command=`, y este a su vez la delega al servicio. Esa cadena mantiene cada capa con una única responsabilidad: la vista captura y muestra, el servicio valida y decide, y `ArchivoServicio` persiste. Además, replantear la interfaz con un sidebar, formularios y tablas agrupados en contenedores con título, y una paleta coherente con el logo, mejoró la claridad y la consistencia visual respecto a la versión anterior.