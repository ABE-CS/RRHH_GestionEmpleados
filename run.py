from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'hadassah1'

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="Hadassah",       # Cambia por tu usuario MySQL
        password="Root",       # Cambia por tu contraseña MySQL
        database="rrhh"        # Nombre de tu base de datos
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
    return render_template('home.html')

@app.route('/lista-empleados')
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
        documento = request.form['documento']
        email = request.form['email']
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        fecha_ingreso = request.form['fecha_ingreso']
        cargo = request.form['cargo']
        salario = request.form.get('salario')
        

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO empleados (nombre, cargo) VALUES (%s, %s)", (nombre, cargo))
        conexion.commit()
        cursor.close()
        conexion.close()
        
        flash('✅ Nuevo empleado registrado correctamente')
        return redirect('/lista-empleados')
    return render_template('registrar_empleado.html')

@app.route('/editar-empleado/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        datos = (
            request.form['nombre'],
            request.form['documento'],
            request.form['email'],
            request.form['telefono'],
            request.form['direccion'],
            request.form['fecha_ingreso'],
            request.form['cargo'],
            request.form['salario'],
            id
        )
        cursor.execute("""
            UPDATE empleados SET nombre=%s, documento=%s, email=%s, telefono=%s, direccion=%s,
            fecha_ingreso=%s, cargo=%s, salario=%s WHERE id=%s
        """, datos)
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('✅ Empleado editado correctamente')
        return redirect('/lista-empleados')
    else:
        cursor.execute("SELECT * FROM empleados WHERE id = %s", (id,))
        empleado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if empleado:
            return render_template('editar_empleado.html', empleado=empleado)
        else:
            return "Empleado no encontrado", 404

@app.route('/eliminar-empleado/<int:id>', methods=['GET'])
def eliminar_empleado(id):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM empleados WHERE id = %s", (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('🗑 Empleado eliminado correctamente')
    except mysql.connector.Error as err:
        flash(f'❌ Error al eliminar el empleado: {err}')
    return redirect('/lista-empleados')        



if __name__ == '__main__':
    app.run(debug=True)
