from flask import Flask, request, jsonify
from flask_cors import CORS
from conexion import ConexionDB

db = ConexionDB(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME")
)

app = Flask(__name__)
CORS(app)  # Me tienen podrido con el CORS, 
#pero bueno, es lo que hay. No me da tiempo a hacer 
#un proxy inverso ni nada de eso.

@app.route("/prueba")
def prueba():
    return jsonify({"mensaje": "Flask funciona correctamente"})

@app.route("/productos", methods=["GET"])
def get_productos():
    es_admin = request.args.get("admin") == "true"
    
    cursor = db.obtener_cursor()
    if es_admin:
        cursor.execute("""
            SELECT id_producto, nombre, descripcion, precio, stock, color, estado, imagen_url
            FROM Productos
        """)
    else:
        cursor.execute("""
            SELECT id_producto, nombre, descripcion, precio, stock, color, estado, imagen_url
            FROM Productos
            WHERE estado = 'activo'
        """)
        
    rows = cursor.fetchall()
    cursor.close()

    productos = []
    for row in rows:
        productos.append({
            "id": row["id_producto"],
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": float(row["precio"]),
            "stock": row["stock"],
            "color": row["color"],
            "estado": row["estado"],
            "imagen": row["imagen_url"]
        })

    return jsonify(productos)
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, stock, color, estado, imagen_url
        FROM Productos
        WHERE estado = 'activo'
    """)
    rows = cursor.fetchall()
    cursor.close()

    productos = []
    for row in rows:
        productos.append({
            "id": row["id_producto"],
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": float(row["precio"]),
            "stock": row["stock"],
            "color": row["color"],
            "estado": row["estado"],
            "imagen": row["imagen_url"]
        })

    return jsonify(productos)

@app.route("/productos/<int:id>", methods=["GET"])
def get_producto(id):
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, stock, color, estado, imagen_url
        FROM Productos
        WHERE id_producto = %s
    """, (id,)) 
    row = cursor.fetchone()
    cursor.close()

    if row:
        producto = {
            "id": row["id_producto"],
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": float(row["precio"]),
            "stock": row["stock"],
            "color": row["color"],
            "estado": row["estado"],
            "imagen": row["imagen_url"]
        }
        return jsonify(producto)
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

@app.route("/carrito/<int:id>", methods=["GET"])
def get_carrito(id):
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT cd.id_detalle, p.nombre, p.imagen_url, cd.cantidad, cd.precio_unitario
        FROM CarritoDetalle cd
        JOIN Carrito c ON cd.id_carrito = c.id_carrito
        JOIN Productos p ON cd.id_producto = p.id_producto
        WHERE c.id_usuario = %s
    """, (id,))
    rows = cursor.fetchall()
    cursor.close()

    carrito = []
    total = 0
    for row in rows:
        subtotal = float(row["precio_unitario"]) * row["cantidad"]
        total += subtotal
        carrito.append({
            "id_detalle": row["id_detalle"],
            "nombre": row["nombre"],
            "imagen": row["imagen_url"],
            "cantidad": row["cantidad"],
            "precio_unitario": float(row["precio_unitario"]),
            "subtotal": subtotal
        })

    return jsonify({"items": carrito, "total": total})


@app.route("/carrito/agregar", methods=["POST"])
def agregar_carrito():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No se recibió payload JSON"}), 400

        id_producto = data.get("id_producto")
        cantidad = data.get("cantidad", 1)

        if not id_producto:
            return jsonify({"error": "No se envió id_producto"}), 400

        conexion = db.conectar()
        cursor = conexion.cursor(dictionary=True) 

        # Usuario hardcodeado = 1
        cursor.execute("SELECT id_carrito FROM Carrito WHERE id_usuario = %s", (1,))
        carrito = cursor.fetchone()

        if not carrito:
            cursor.close()
            return jsonify({"error": "No existe carrito para el id_usuario 1. Crea el registro en la BD primero."}), 400

        id_carrito = carrito["id_carrito"]

        cursor.execute(
            "SELECT id_detalle, cantidad FROM CarritoDetalle WHERE id_carrito = %s AND id_producto = %s",
            (id_carrito, id_producto)
        )
        item = cursor.fetchone()

        if item:
            cursor.execute(
                "UPDATE CarritoDetalle SET cantidad = cantidad + %s WHERE id_detalle = %s",
                (cantidad, item["id_detalle"])
            )
        else:
            cursor.execute("SELECT precio FROM Productos WHERE id_producto = %s", (id_producto,))
            prod = cursor.fetchone()
            if not prod:
                cursor.close()
                return jsonify({"error": "El producto especificado no existe en la BD"}), 404

            cursor.execute(
                "INSERT INTO CarritoDetalle (id_carrito, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                (id_carrito, id_producto, cantidad, prod["precio"])
            )

        conexion.commit() 
        cursor.close()

        return jsonify({"message": "Producto agregado exitosamente"}), 200

    except Exception as e:
        print(f"Error interno en /carrito/agregar: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/carrito/eliminar/<int:id_detalle>", methods=["DELETE", "POST"])
def eliminar_item_carrito(id_detalle):
    try:
        conexion = db.conectar()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM CarritoDetalle WHERE id_detalle = %s", (id_detalle,))
        
        conexion.commit()
        cursor.close()

        return jsonify({"message": "Producto eliminado del carrito exitosamente"}), 200

    except Exception as e:
        print(f"Error al eliminar ítem: {e}")
        return jsonify({"error": str(e)}), 500

#------------------------------------------------------------------

@app.route("/registro", methods=["POST"])
def registrar_usuario():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No se recibió payload JSON"}), 400

        nombre = data.get("nombre")
        correo = data.get("correo")
        usuario = data.get("usuario")
        contrasena = data.get("contrasena")

        if not all([nombre, correo, usuario, contrasena]):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        conexion = db.conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT id_usuario FROM Usuarios WHERE usuario = %s OR correo = %s",
            (usuario, correo)
        )
        existente = cursor.fetchone()

        if existente:
            cursor.close()
            return jsonify({"error": "El nombre de usuario o el correo ya están registrados."}), 400

        cursor.execute(
            """
            INSERT INTO Usuarios (nombre, correo, usuario, contrasena, rol)
            VALUES (%s, %s, %s, %s, 'admin')
            """,
            (nombre, correo, usuario, contrasena)
        )
        conexion.commit()
        cursor.close()

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        print(f"Error interno en /registro: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login_admin():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No se recibió payload JSON"}), 400

        usuario = data.get("usuario")
        contrasena = data.get("contrasena")

        if not usuario or not contrasena:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        conexion = db.conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT id_usuario, nombre, correo, usuario, contrasena, rol FROM Usuarios WHERE usuario = %s",
            (usuario,)
        )
        admin = cursor.fetchone()
        cursor.close()

        if not admin or admin["contrasena"] != contrasena:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        return jsonify({
            "message": "Bienvenido",
            "usuario": {
                "id": admin["id_usuario"],
                "nombre": admin["nombre"],
                "correo": admin["correo"],
                "usuario": admin["usuario"],
                "rol": admin["rol"]
            }
        }), 200

    except Exception as e:
        print(f"Error interno en /login: {e}")
        return jsonify({"error": str(e)}), 500
#----------------------------------------------------------------
@app.route("/productos/editar/<int:id>", methods=["PUT"])
def editar_producto(id):
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No se recibió payload JSON"}), 400

        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        precio = data.get("precio")
        stock = data.get("stock")
        color = data.get("color")
        estado = data.get("estado")
        imagen = data.get("imagen")

        conexion = db.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE Productos 
            SET nombre = %s, descripcion = %s, precio = %s, stock = %s, color = %s, estado = %s, imagen_url = %s
            WHERE id_producto = %s
            """,
            (nombre, descripcion, precio, stock, color, estado, imagen, id)
        )
        conexion.commit()
        cursor.close()

        return jsonify({"message": "Producto actualizado exitosamente"}), 200

    except Exception as e:
        print(f"Error interno al editar producto: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/productos/agregar", methods=["POST"])
def agregar_producto():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No se recibió payload JSON"}), 400

        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        precio = data.get("precio")
        stock = data.get("stock")
        color = data.get("color")
        estado = data.get("estado", "activo")
        imagen = data.get("imagen")

        if not all([nombre, descripcion, precio is not None, stock is not None]):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        conexion = db.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO Productos (nombre, descripcion, precio, stock, color, estado, imagen_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (nombre, descripcion, precio, stock, color, estado, imagen)
        )
        conexion.commit()
        cursor.close()

        return jsonify({"message": "Producto creado exitosamente"}), 201

    except Exception as e:
        print(f"Error interno al agregar producto: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/productos/eliminar/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    try:
        conexion = db.conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_producto FROM Productos WHERE id_producto = %s", (id,))
        producto = cursor.fetchone()

        if not producto:
            cursor.close()
            return jsonify({"error": "El producto no existe"}), 404

        cursor.execute("DELETE FROM Productos WHERE id_producto = %s", (id,))
        conexion.commit()
        cursor.close()

        return jsonify({"message": "Producto eliminado exitosamente"}), 200

    except Exception as e:
        print(f"Error interno al eliminar producto: {e}")
        return jsonify({"error": str(e)}), 500
#SUELTENMEEEEEEEEEEEEEEEEEEE--------------------------
@app.route("/reportes", methods=["GET"])
def get_reportes():
    try:
        cursor = db.obtener_cursor()
        
        cursor.execute("""
            SELECT cd.id_detalle, u.nombre AS cliente, p.nombre AS producto, 
                   cd.cantidad, cd.precio_unitario
            FROM CarritoDetalle cd
            JOIN Carrito c ON cd.id_carrito = c.id_carrito
            JOIN Usuarios u ON c.id_usuario = u.id_usuario
            JOIN Productos p ON cd.id_producto = p.id_producto
        """)
        rows = cursor.fetchall()
        cursor.close()

        reportes = []
        for row in rows:
            subtotal = float(row["precio_unitario"]) * row["cantidad"]
            reportes.append({
                "id_detalle": f"#TX-{row['id_detalle']}",
                "cliente": row["cliente"],
                "producto": row["producto"],
                "cantidad": row["cantidad"],
                "precio_unitario": float(row["precio_unitario"]),
                "subtotal": subtotal
            })

        return jsonify(reportes), 200

    except Exception as e:
        print(f"Error interno en /reportes: {e}")
        return jsonify({"error": str(e)}), 500
#SUELTENMEEEEEEEEEEEEEEEEEEE--------------------------X2
@app.route("/carrito/comprar/<int:id_usuario>", methods=["POST"])
def realizar_compra(id_usuario):
    conexion = db.conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id_carrito FROM Carrito WHERE id_usuario = %s", (id_usuario,))
        carrito = cursor.fetchone()
        
        if not carrito:
            return jsonify({"error": "No se encontró un carrito activo para este usuario"}), 404
            
        id_carrito = carrito[0] if isinstance(carrito, tuple) else carrito["id_carrito"]

        cursor.execute("""
            SELECT id_producto, cantidad, precio_unitario 
            FROM CarritoDetalle WHERE id_carrito = %s
        """, (id_carrito,))
        items = cursor.fetchall()

        if not items:
            return jsonify({"error": "El carrito está vacío"}), 400

        total_orden = 0
        for item in items:
            # Soportar tanto tupla como diccionario según el cursor
            id_prod = item[0] if isinstance(item, tuple) else item["id_producto"]
            cant = item[1] if isinstance(item, tuple) else item["cantidad"]
            precio_uni = item[2] if isinstance(item, tuple) else item["precio_unitario"]

            cursor.execute("SELECT stock, nombre FROM Productos WHERE id_producto = %s", (id_prod,))
            prod = cursor.fetchone()
            
            stock_actual = prod[0] if isinstance(prod, tuple) else prod["stock"]
            nombre_prod = prod[1] if isinstance(prod, tuple) else prod["nombre"]

            if stock_actual < cant:
                return jsonify({"error": f"Stock insuficiente para el producto: {nombre_prod}"}), 400
            
            total_orden += float(precio_uni) * cant

        cursor.execute("""
            INSERT INTO Ordenes (id_usuario, total, estado) 
            VALUES (%s, %s, 'pagado')
        """, (id_usuario, total_orden))
        id_orden = cursor.lastrowid

        for item in items:
            id_prod = item[0] if isinstance(item, tuple) else item["id_producto"]
            cant = item[1] if isinstance(item, tuple) else item["cantidad"]
            precio_uni = item[2] if isinstance(item, tuple) else item["precio_unitario"]

            cursor.execute("""
                INSERT INTO OrdenDetalle (id_orden, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """, (id_orden, id_prod, cant, precio_uni))

            cursor.execute("""
                UPDATE Productos 
                SET stock = stock - %s,
                    estado = CASE WHEN (stock - %s) <= 0 THEN 'inactivo' ELSE estado END
                WHERE id_producto = %s
            """, (cant, cant, id_prod))

        cursor.execute("DELETE FROM CarritoDetalle WHERE id_carrito = %s", (id_carrito,))

        conexion.commit()
        cursor.close()

        return jsonify({"message": "Compra procesada con éxito", "id_orden": id_orden}), 200

    except Exception as e:
        conexion.rollback()
        cursor.close()
        print(f"Error interno al realizar compra: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)