from flask import Flask, render_template, request, jsonify
from conexion import ConexionDB

db = ConexionDB(
    host="bdppw.mysql.database.azure.com",
    user="Hunter774575",
    password="Darkhunter77*",
    db="xbits"
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detalle/<int:id>")
def detalle(id):
    return render_template("detalle.html", id=id)

@app.route("/carrito")
def carrito():
    return render_template("carrito.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/terminos")
def terminos():
    return render_template("terminos.html")

@app.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")

@app.route("/Reportes")
def reportes():
    return render_template("Reportes.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/nuevoProducto")
def nuevo_producto():
    return render_template("nuevoProducto.html")

# Precaucion
# Aqui abajo hay un desorden ajajajajajaja
#-----------------------------------------------------------------------

@app.route("/productos", methods=["GET"])
def get_productos():
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, imagen_url
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
            "imagen": row["imagen_url"]
        })

    return jsonify(productos)


@app.route("/productos/<int:id>", methods=["GET"])
def get_producto(id):
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, imagen_url
        FROM Productos
        WHERE id_producto = %s AND estado = 'activo'
    """, (id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        producto = {
            "id": row["id_producto"],
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": float(row["precio"]),
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
#-----------------------------------------------------------
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

if __name__ == "__main__":
    app.run()


