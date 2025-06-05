import pytest
from run import app, conectar_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    # Opcional: valida contenido que esperes ver en home.html
    # assert b"Bienvenido" in response.data

def test_empleados(client):
    response = client.get('/empleados')
    assert response.status_code == 200
    # Opcional: valida que "Empleados" o texto similar esté en la página
    # assert b"Empleados" in response.data

def test_registrar_empleado(client):
    # Envía datos para registrar un empleado de prueba
    response = client.post('/registrar-empleado', data={
        'nombre': 'Juan Perez',
        'cargo': 'Analista'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Valida que el nombre del empleado nuevo esté en la respuesta HTML
    assert b'Juan Perez' in response.data

def test_db_connection():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT 1")
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    assert resultado == (1,)
