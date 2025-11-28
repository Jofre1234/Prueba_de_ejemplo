from flask import Flask, request, jsonify
import pytest

app = Flask(__name__)

# Ruta principal
@app.route('/')
def hello_world():
    return "¡Hola! Mi prueba final Jofre Bedón!"

# Ruta mínima de IA
@app.route('/ai', methods=['POST'])
def ai():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"response": "Por favor envía un prompt."})
    return jsonify({"response": f"Respuesta generada para: {prompt}"})


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
        assert "Jofre Bedón".encode() in response.data

    def test_ai(client):
        response = client.post('/ai', json={"prompt": "Hola"})
        assert response.status_code == 200
        assert "Hola" in response.get_json()["response"]

    pytest.main([__file__])


if __name__ == '__main__':
    import sys
    if "test" in sys.argv:
        run_tests()  # Ejecuta las pruebas con: python app.py test
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
