from flask import Flask
import pytest

app = Flask(__name__)

# Ruta principal
@app.route('/')
def hello_world():
    return "hola me llamo jofre y este es mi prueba de axamen"

# === PRUEBAS AUTOMATIZADAS ===
def run_tests():
    @pytest.fixture
    def client():
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_home(client):
        response = client.get('/')
        assert response.status_code == 200
        # Verificamos que tu mensaje salga correctamente
        assert "hola me llamo jofre".encode() in response.data

    pytest.main([__file__])


if __name__ == '__main__':
    import sys
    if "test" in sys.argv:
        run_tests()  # Ejecuta las pruebas con: python app.py test
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)