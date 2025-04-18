import sqlite3
import os

def init_db():
    # Eliminar la base de datos existente si existe
    if os.path.exists('database.db'):
        os.remove('database.db')
        
    # Crear una nueva conexión a la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    # Crear tabla de productos
    cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT
    )
    ''')
    
    # Crear tabla de comentarios
    cursor.execute('''
    CREATE TABLE comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    # Insertar datos de ejemplo - Usuarios
    users = [
        ('admin', 'admin123', 'admin@example.com', 'admin'),
        ('user1', 'password123', 'user1@example.com', 'user'),
        ('user2', 'password456', 'user2@example.com', 'user')
    ]
    cursor.executemany('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', users)
    
    # Insertar datos de ejemplo - Productos
    products = [
        ('Laptop Gaming', 'Laptop potente para gamers', 1299.99, 'Electrónica'),
        ('Smartphone', 'Último modelo con cámara de alta resolución', 899.99, 'Electrónica'),
        ('Auriculares Bluetooth', 'Auriculares inalámbricos con cancelación de ruido', 149.99, 'Accesorios'),
        ('Monitor 4K', 'Monitor de alta resolución para profesionales', 499.99, 'Electrónica'),
        ('Teclado Mecánico', 'Teclado gaming con switches Cherry MX', 129.99, 'Accesorios')
    ]
    cursor.executemany('INSERT INTO products (name, description, price, category) VALUES (?, ?, ?, ?)', products)
    
    # Insertar datos de ejemplo - Comentarios
    comments = [
        (1, 'user1', 'Excelente laptop, muy rápida!'),
        (1, 'user2', 'El precio es un poco alto pero vale la pena'),
        (2, 'user1', 'La cámara es impresionante'),
        (3, 'user2', 'La calidad de sonido es increíble'),
        (4, 'user1', 'Los colores son muy precisos')
    ]
    cursor.executemany('INSERT INTO comments (product_id, username, comment) VALUES (?, ?, ?)', comments)
    
    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    
    print('Base de datos inicializada correctamente')

if __name__ == '__main__':
    init_db()