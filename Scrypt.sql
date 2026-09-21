-- Crear la base de datos
DROP DATABASE IF EXISTS xbits;
CREATE DATABASE xbits;
USE xbits;

-- 1. Tabla de usuarios
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('cliente','admin') DEFAULT 'cliente'
);

-- 2. Tabla de productos
CREATE TABLE Productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    color VARCHAR(50),
    estado ENUM('activo','inactivo') DEFAULT 'activo',
    imagen_url VARCHAR(255)
);

-- 3. Tabla de carritos
CREATE TABLE Carrito (
    id_carrito INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- 4. Detalle del carrito
CREATE TABLE CarritoDetalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_carrito INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_carrito) REFERENCES Carrito(id_carrito),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- 5. Tabla de órdenes
CREATE TABLE Ordenes (
    id_orden INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente','pagado','enviado') DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- 6. Detalle de órdenes
CREATE TABLE OrdenDetalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_orden INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_orden) REFERENCES Ordenes(id_orden),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- 7. Tabla independiente para los reportes históricos de compras
CREATE TABLE Reportes (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre_cliente VARCHAR(100) NOT NULL,
    nombre_producto VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger que captura lo que estaba en el carrito justo antes de borrarlo 
-- y lo archiva permanentemente en la tabla 'Reportes'
DELIMITER //

-- Ni modo a esto tuve que llegar :,v
CREATE TRIGGER trg_guardar_reporte_compra
BEFORE DELETE ON CarritoDetalle
FOR EACH ROW
BEGIN
    DECLARE v_nombre_cliente VARCHAR(100);
    DECLARE v_nombre_producto VARCHAR(100);
    
    -- Obtenemos el nombre del cliente a través del carrito
    SELECT u.nombre INTO v_nombre_cliente
    FROM Carrito c
    JOIN Usuarios u ON c.id_usuario = u.id_usuario
    WHERE c.id_carrito = OLD.id_carrito;
    
    -- Obtenemos el nombre del producto
    SELECT nombre INTO v_nombre_producto
    FROM Productos
    WHERE id_producto = OLD.id_producto;
    
    -- Insertamos el registro histórico independiente
    INSERT INTO Reportes (id_usuario, nombre_cliente, nombre_producto, cantidad, precio_unitario, subtotal)
    SELECT c.id_usuario, v_nombre_cliente, v_nombre_producto, OLD.cantidad, OLD.precio_unitario, (OLD.cantidad * OLD.precio_unitario)
    FROM Carrito c
    WHERE c.id_carrito = OLD.id_carrito;
END;
//

DELIMITER ;

-- ==========================================
-- INSERTS DE DATOS DE PRUEBA
-- ==========================================

-- Inserción de Productos
INSERT INTO Productos (id_producto, nombre, descripcion, precio, stock, color, estado, imagen_url) VALUES 
(1, 'Laptop Gamer', 'Computadora portátil para estudio, trabajo y entretenimiento.', 1200.00, 10, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),
(2, 'Smartphone 5G', 'Teléfono inteligente con conectividad 5G y pantalla moderna.', 800.00, 20, 'Azul', 'activo', 'https://m.media-amazon.com/images/I/71pszRoOwUL._AC_SY741_.jpg'),
(3, 'Audífonos Bluetooth', 'Auriculares inalámbricos con estuche de carga digital.', 150.00, 30, 'Blanco', 'activo', 'https://m.media-amazon.com/images/I/31yq9PU7LDL._SS400_.jpg'),
(4, 'Monitor Full HD 24"', 'Monitor LED de 24 pulgadas con resolución Full HD.', 180.00, 15, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),
(5, 'Teclado Mecánico RGB', 'Teclado retroiluminado con switches mecánicos.', 60.00, 25, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),
(6, 'Mouse Inalámbrico', 'Mouse ergonómico con conexión inalámbrica.', 25.50, 50, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),
(7, 'Tarjeta Gráfica RTX 4060', 'GPU de alto rendimiento para gaming y diseño gráfico.', 350.00, 8, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),
(8, 'Memoria RAM 16GB DDR5', 'Módulo de memoria ultrarrápida para equipos modernos.', 75.00, 40, 'Gris', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),
(9, 'Procesador AMD Ryzen 7 5800X', 'Procesador de 8 núcleos y 16 hilos ideal para multitarea.', 280.00, 12, 'Plateado', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg');

-- Inserción de Usuarios
INSERT INTO Usuarios (id_usuario, nombre, correo, usuario, contrasena, rol) VALUES 
(1, 'Usuario Local', 'local@xuclebits.com', 'localuser', '1234', 'cliente'),
(2, 'Roberto Zelaya', 'roberto@rocketmail.com', 'ElTreintayOcho', 'qwerty', 'admin'),
(3, 'Roberto Admin', 'tumama@gmail.com', 'qwerty', 'qwerty', 'admin'),
(4, 'Carlos Mendoza', 'carlos@gmail.com', 'cmendoza', '1234', 'cliente'),
(5, 'Ana Rodríguez', 'ana@gmail.com', 'arodriguez', '1234', 'cliente');

-- Inserción de Carritos (uno por cada usuario para mantener la consistencia)
INSERT INTO Carrito (id_carrito, id_usuario) VALUES 
(1, 1),
(2, 4),
(3, 5);


INSERT INTO Reportes (id_usuario, nombre_cliente, nombre_producto, cantidad, precio_unitario, subtotal) VALUES 
(4, 'Carlos Mendoza', 'Tarjeta Gráfica RTX 4060', 1, 350.00, 350.00),
(4, 'Carlos Mendoza', 'Mouse Inalámbrico', 2, 25.50, 51.00),
(5, 'Ana Rodríguez', 'Procesador AMD Ryzen 7 5800X', 1, 280.00, 280.00),
(5, 'Ana Rodríguez', 'Memoria RAM 16GB DDR5', 2, 75.00, 150.00),
(1, 'Usuario Local', 'Laptop Gamer', 1, 1200.00, 1200.00);



select * from productos;
select * from carritodetalle;
