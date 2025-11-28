from flask import Flask, request, jsonify
import pytest

app = Flask(__name__)

# Ruta principal (Tu presentación)
@app.route('/')
def hello_world():
    return "hola me llamo jofre y este es mi prueba de axamen de IA"

# Ruta de Chat con IA
@app.route('/ai', methods=['POST'])
def ai():
    # Recibimos el mensaje del usuario
    data = request.json
    prompt = data.get("prompt", "")
    
    # Si no envían nada, pedimos un prompt
    if not prompt:
        return jsonify({"response": "Por favor envía un prompt."})
    
    # Aquí devolvemos la respuesta simulada
    return jsonify({"response": f"Respuesta de IA para: {prompt}"})


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
        # Verificamos que tu nombre esté en la respuesta
        assert "jofre".encode() in response.data

    def test_ai(client):
        # Probamos que el chat responda correctamente
        response = client.post('/ai', json={"prompt": "Hola"})
        assert response.status_code == 200
        assert "Respuesta de IA".encode() in response.data

    pytest.main([__file__])


if __name__ == '__main__':
    import sys
    if "test" in sys.argv:
        run_tests()  # Ejecuta las pruebas con: python app.py test
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)