import mysql.connector
from datetime import datetime, timedelta

def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto si tienes un usuario diferente
        password="",  # Cambia esto si tienes una contraseña configurada
        database="app_db"
    )
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            rh VARCHAR(5) NOT NULL,
            sexo VARCHAR(10) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            especialidad VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordenes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT,
            doctor_id INT NOT NULL,
            fecha DATETIME NOT NULL,
            cubiculo VARCHAR(50) NOT NULL,
            estado VARCHAR(50) NOT NULL DEFAULT 'Disponible',
            usuario_id INT, -- Nuevo campo para almacenar el ID del usuario
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (doctor_id) REFERENCES doctores (id)
        )
    ''')

    # Verificar si la columna cliente_id ya existe en la tabla usuarios
    cursor.execute('''
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'cliente_id'
    ''')
    if cursor.fetchone()[0] == 0:
        # Agregar la columna cliente_id a la tabla usuarios
        cursor.execute('''
            ALTER TABLE usuarios
            ADD COLUMN cliente_id INT,
            ADD FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        ''')

    # Verificar si la columna apellido ya existe en la tabla doctores
    cursor.execute('''
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'doctores' AND COLUMN_NAME = 'apellido'
    ''')
    if cursor.fetchone()[0] == 0:
        # Agregar la columna apellido a la tabla doctores
        cursor.execute('''
            ALTER TABLE doctores
            ADD COLUMN apellido VARCHAR(255) NOT NULL
        ''')
    
    # Insertar datos iniciales
    cursor.execute('''
        INSERT IGNORE INTO clientes (nombre, apellido, email, telefono, rh, sexo)
        VALUES 
        ('Juan', 'Pérez', 'juan@example.com', '1234567890', 'O+', 'Masculino'),
        ('María', 'Gómez', 'maria@example.com', '0987654321', 'A-', 'Femenino')
    ''')
    cursor.execute('''
        INSERT IGNORE INTO usuarios (username, password, role, cliente_id)
        VALUES 
        ('juan', '1234', 'user', 1),  -- Relacionado con el cliente Juan Pérez
        ('doctor', '2345', 'doctor', NULL)  -- Sin relación con clientes
    ''')

    # Verificar si ya existen doctores en la base de datos
    cursor.execute('SELECT nombre FROM doctores')
    existing_doctors = {row[0] for row in cursor.fetchall()}  # Obtener nombres existentes

    # Insertar los 5 doctores de Medicina General solo si no existen
    doctores = [
        ('Dr. José', 'Martínez', 'Medicina General'),
        ('Dra. Laura', 'Rodríguez', 'Medicina General'),
        ('Dr. Andrés', 'Gómez', 'Medicina General'),
        ('Dra. Sofía', 'Ramírez', 'Medicina General'),
        ('Dr. Miguel', 'Torres', 'Medicina General')
    ]
    for doctor in doctores:
        cursor.execute('SELECT COUNT(*) FROM doctores WHERE nombre = %s AND apellido = %s', (doctor[0], doctor[1]))
        if cursor.fetchone()[0] == 0:  # Verificar si el doctor ya existe
            cursor.execute('''
                INSERT INTO doctores (nombre, apellido, especialidad)
                VALUES (%s, %s, %s)
            ''', (doctor[0], doctor[1], doctor[2]))

        # Crear un usuario para cada doctor
        cursor.execute('''
            INSERT IGNORE INTO usuarios (username, password, role)
            VALUES (%s, %s, 'doctor')
        ''', (doctor[0], '2345'))

    # Insertar 5 doctores únicos por cada especialidad
    especialidades = ['Cardiología', 'Pediatría', 'Ginecología', 'Neurología', 'Psiquiatría']
    doctores_por_especialidad = [
        ('Carlos', 'Hernández'),
        ('Ana', 'Martínez'),
        ('Luis', 'Gómez'),
        ('María', 'Rodríguez'),
        ('Pedro', 'Ramírez')
    ]

    for especialidad in especialidades:
        for doctor in doctores_por_especialidad:
            nombre = doctor[0]
            apellido = doctor[1]
            cursor.execute('SELECT COUNT(*) FROM doctores WHERE nombre = %s AND apellido = %s AND especialidad = %s',
                           (nombre, apellido, especialidad))
            if cursor.fetchone()[0] == 0:  # Verificar si el doctor ya existe
                cursor.execute('''
                    INSERT INTO doctores (nombre, apellido, especialidad)
                    VALUES (%s, %s, %s)
                ''', (nombre, apellido, especialidad))

                # Crear un usuario para cada doctor
                cursor.execute('''
                    INSERT IGNORE INTO usuarios (username, password, role)
                    VALUES (%s, %s, 'doctor')
                ''', (nombre, '2345'))

                # Obtener el ID del doctor recién insertado
                cursor.execute('SELECT id FROM doctores WHERE nombre = %s AND apellido = %s AND especialidad = %s',
                               (nombre, apellido, especialidad))
                doctor_id = cursor.fetchone()[0]

                # Asignar 5 citas únicas al doctor
                for j in range(5):
                    fecha = (datetime.now() + timedelta(days=j)).strftime('%Y-%m-%d %H:%M:%S')
                    cubiculo = f'Cubículo {j + 1}'
                    cursor.execute('''
                        INSERT INTO citas (doctor_id, fecha, cubiculo, estado)
                        VALUES (%s, %s, %s, %s)
                    ''', (doctor_id, fecha, cubiculo, 'Disponible'))

    conn.commit()
    conn.close()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto si tienes un usuario diferente
        password="",  # Cambia esto si tienes una contraseña configurada
        database="app_db"
    )
