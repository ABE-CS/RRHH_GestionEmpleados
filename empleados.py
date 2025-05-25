import mysql.connector

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="Hadassah",        # Cambia a tu usuario MySQL
        password="Root",        # Cambia a tu contraseña MySQL
        database="rrhh"         # Tu base de datos
    )

def obtener_empleados():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return empleados

def insertar_empleado(nombre, cargo):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO empleados (nombre, cargo) VALUES (%s, %s)", (nombre, cargo))
    conexion.commit()
    cursor.close()
    conexion.close()
