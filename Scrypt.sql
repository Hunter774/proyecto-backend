-- Crear la base de datos
DROP DATABASE IF exists XBits;
CREATE DATABASE XBits;
USE XBits;

-- Tabla de usuarios
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('cliente','admin') DEFAULT 'cliente'
);

-- Tabla de productos
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

-- Tabla de carritos
CREATE TABLE Carrito (
    id_carrito INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Detalle del carrito
CREATE TABLE CarritoDetalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_carrito INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_carrito) REFERENCES Carrito(id_carrito),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- Tabla de órdenes
CREATE TABLE Ordenes (
    id_orden INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente','pagado','enviado') DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Detalle de órdenes
CREATE TABLE OrdenDetalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_orden INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_orden) REFERENCES Ordenes(id_orden),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- Productos del index probamos mas despues jeje
INSERT INTO Productos (nombre, descripcion, precio, stock, color, estado, imagen_url)
VALUES 
('Laptop Gamer', 'Computadora portátil para estudio, trabajo y entretenimiento.', 1200.00, 10, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),

('Smartphone 5G', 'Teléfono inteligente con conectividad 5G y pantalla moderna.', 800.00, 20, 'Azul', 'activo', 'https://m.media-amazon.com/images/I/71pszRoOwUL._AC_SY741_.jpg'),

('Audífonos Bluetooth', 'Auriculares inalámbricos con estuche de carga digital.', 150.00, 30, 'Blanco', 'activo', 'https://m.media-amazon.com/images/I/31yq9PU7LDL._SS400_.jpg');

-- Extras para ampliar catálogo
INSERT INTO Productos (nombre, descripcion, precio, stock, color, estado, imagen_url)
VALUES
('Monitor Full HD 24"', 'Monitor LED de 24 pulgadas con resolución Full HD.', 180.00, 15, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),

('Teclado Mecánico RGB', 'Teclado retroiluminado con switches mecánicos.', 60.00, 25, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg'),

('Mouse Inalámbrico', 'Mouse ergonómico con conexión inalámbrica.', 25.50, 50, 'Negro', 'activo', 'https://m.media-amazon.com/images/I/71EjPGMpNgL._AC_SX679_.jpg');

select * from Productos;

-- Usuario local fijo
INSERT INTO Usuarios (nombre, correo, usuario, contrasena, rol)
VALUES ('Usuario Local', 'local@xuclebits.com', 'localuser', '1234', 'cliente');

-- Carrito asociado al usuario local (id_usuario = 1)
INSERT INTO Carrito (id_usuario)
VALUES (1);

-- Detalle del carrito con productos iniciales
INSERT INTO CarritoDetalle (id_carrito, id_producto, cantidad, precio_unitario)
VALUES
(1, 1, 1, 1200.00),  -- Laptop Gamer
(1, 2, 1, 800.00);   -- Smartphone 5G

SELECT cd.id_detalle, p.nombre, p.imagen_url, cd.cantidad, cd.precio_unitario
        FROM CarritoDetalle cd
        JOIN Carrito c ON cd.id_carrito = c.id_carrito
        JOIN Productos p ON cd.id_producto = p.id_producto
        WHERE c.id_usuario = 1
        ;
        
select * from CarritoDetalle;
