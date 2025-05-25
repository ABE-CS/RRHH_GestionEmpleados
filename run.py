from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="Hadassah",        # Cambia por tu usuario MySQL
        password="Root",        # Cambia por tu contraseña MySQL
        database="rrhh"         # Nombre de tu base de datos
    )

@app.route('/test-db')
def test_db():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return f"Conexión exitosa! Resultado de la consulta: {resultado}"
    except mysql.connector.Error as err:
        return f"Error al conectar a la base de datos: {err}"

@app.route('/')
def home():
    return render_template('home.html')  # Página principal con tu home.html

@app.route('/empleados')
def empleados():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('lista_empleados.html', empleados=empleados)

@app.route('/registrar-empleado', methods=['GET', 'POST'])
def registrar_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cargo = request.form['cargo']

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO empleados (nombre, cargo) VALUES (%s, %s)", (nombre, cargo))
        conexion.commit()
        cursor.close()
        conexion.close()

        return redirect('/empleados')  # Redirigir a la lista de empleados
    return render_template('registrar_empleado.html')

if __name__ == '__main__':
    app.run(debug=True)

