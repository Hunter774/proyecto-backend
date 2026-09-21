
# Proyecto Final Programación Web
**Tienda en Linea - Xucle-Bits**

(Grupo ??)
- Roberto Antonio Matamoros Zelaya

## Objetivo
Diseñar e implementar una aplicacion web funcional para una tienda en línea de **tecnologia**, integrando los conceptos aprendidos durante el curso.

## Estructura del Proyecto
```text
Proyecto_Programacion_Web_Grupo_1-main
│
├── index.html
├── style.css
│
├── icons
│   └── Icono.png
│
└── componentes
    ├── carrito.html
    ├── carrito.css
    ├── detalle.html
    ├── login.html
    ├── registro.html
    ├── producto.html
    ├── nuevoProducto.html
    ├── editarProducto.html
    ├── Reportes.html
    ├── terminos.html
    └── privacidad.html
```

## Paginas diseñadas (Avance I)
- index.html
  - Página principal de la tienda
  - Logo y nombre de Xucle-Bits
  - Menú de navegación
  - Catálogo de productos
  - Enlaces para visualizar el detalle de los productos
  - Acceso al carrito de compras
  - Enlaces a Términos y Condiciones y Políticas de Privacidad

- detalle.html
  - Vista detallada de un producto
  - Imagen del producto
  - Nombre
  - Precio
  - Descripción
  - Características del producto
  - Botón para agregar al carrito

- carrito.html
  - Vista del carrito de compras
  - Productos seleccionados
  - Precio de los productos
  - Total de la compra
  - Botón para eliminar productos
  - Opción para continuar comprando

- terminos.html
  - Página de Términos y Condiciones

- privacidad.html
  - Página de Políticas de Privacidad

- login.html
  - Formulario de acceso para administradores
  - Campo de usuario
  - Campo de contraseña
  - Enlace para registrar un nuevo administrador

- registro.htm`
  - Formulario para el registro de nuevos administradores

- producto.html
  - Listado de productos
  - Visualización de precios
  - Estado Activo/Inactivo
  - Opciones para agregar, editar y eliminar productos

- nuevoProducto.html
  - Formulario para registrar un nuevo producto
  - Nombre
  - Descripción
  - Precio
  - Cantidad
  - Color
  - Estado
  - Imagen

- editarProducto.html
  - Formulario para modificar un producto
  - Información precargada como ejemplo
  - Opción para guardar los cambios

- Reportes.html
  - Vista de reportes de compras
  - Filtro por fecha inicial y final
  - Búsqueda por ID de compra
  - Tabla para mostrar las compras realizadas

## Paleta de colores
- Fondo: degradado oscuro azul marino (#0d2a4a → #03070d)  
- Texto principal: blanco (#ffffff)  
- Acentos: azul celeste (#4db8ff)  
- Botón Comprar: verde (#00c853 → #009624)  

## Enlaces
- Repositorio (Frontend): https://github.com/Hunter774/Proyecto_Programacion_Web_Grupo_1
-Repostorio (Backend): https://github.com/Hunter774/proyecto-backend
- Despliegue: (No funcional, solo a nivel de BD)

## Entregables
- **Avance I (Semana 5, 23/08/26)** → Diseño grafico de las páginas.  
- **Avance II (Semana 8, 13/09/26)** → Arquitectura basica de manipulacion de datos.  
- **Entrega Final (Semana 10, 21/09/26)** → Proyecto completo con backend y frontend.  

## Segundo Avance - Notas de Desarrollo

**Infraestructura y Despliegue (Azure):** 
  - Se migro correctamente el despliegue de **Static Web** a **Web App**
  - Se configuró y desplegó la infraestructura base del proyecto en la nube, incluyendo la **Web App** y la base de datos **MySQL**.
  - *Estado del despliegue:* Actualmente existe un detalle de conectividad entre la Web App en la nube y la instancia de MySQL. Sin embargo, la conexión a la base de datos desde el entorno local funciona correctamente.
  - *Seguridad:* En esta etapa de pruebas, las credenciales se mantienen directamente en el código base. Para la siguiente entrega se implementará el uso de **variables de entorno (App Settings / Azure Key Vault)** para proteger el acceso. Dado que se trata de un servidor de pruebas aislado, no representa un riesgo para la integridad del sistema.

- **Endpoints e Integración:**
  - Se desarrollaron e integraron exitosamente los endpoints principales para la navegación del cliente: **Index (Catálogo)**, **Detalle de Producto** y **Carrito de Compras**.
  - Los endpoints restantes (Administración y Registro) quedan en desarrollo para el proximo avance.
  - **Dependencias:** Se reemplazó la librería `PyMySQL` por `mysql-connector-python` debido a incompatibilidades y problemas de conexión surgidos en el entorno de Azure. Para instalar la nueva dependencia en el entorno local/virtual, se debe ejecutar:
    ```bash
    pip install mysql-connector-python
    ```

- **Gestión de Usuarios y Carrito:**
  - Para garantizar el flujo funcional de las compras en esta fase, el carrito opera temporalmente con un usuario estático local (`id_usuario = 1`) prefijado en la BD.
  - Este esquema se mantendrá de forma transitoria hasta finalizar la implementación completa del módulo de autenticación y sesiones de usuario ya de ofrma autentica o simulada.

## Tercer Avance y Entrega Final - Notas de Desarrollo

Durante esta etapa final se consolidó el funcionamiento central del sistema, logrando integrar la lógica transaccional en la base de datos y el control dinámico de inventarios. Sin embargo, debido a la carga de trabajo individual y al diseño inicial apresurado del esquema relacional, quedaron pendientes detalles importantes que se documentan a continuación con total honestidad.

- **Arquitectura y Desacoplamiento:** Se llevó a cabo la migración hacia una arquitectura desacoplada a pequeña escala (por capas), separando por completo el backend en Flask como una API REST y el frontend estático mediante solicitudes asíncronas con `fetch`.
- **Lógica Transaccional y Control de Stock:** Se implementó con éxito el procesamiento de compras con commits explícitos, garantizando que al finalizar una transacción se descuenten las unidades del inventario y el producto se inactive automáticamente al llegar a cero stock.
- **Módulo de Reportes:** El reporte de transacciones se limitó a mostrar el listado general; los filtros avanzados por fechas y la búsqueda por ID de compra no se completaron en su totalidad por falta de tiempo y sobrecarga de trabajo individual.
- **Diseño de Base de Datos:** Las relaciones entre `CarritoDetalle`, `Ordenes` y `OrdenDetalle` presentaron inconsistencias iniciales derivadas de un diseño apresurado que requirieron ajustes, evidenciando áreas de mejora en la normalización temprana del esquema.

© 2026 X-Bits - Proyecto Final Programación Web
