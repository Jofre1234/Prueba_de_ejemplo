from flask import Flask, request, jsonify
import pytest

app = Flask(__name__)

# Ruta principal (Tu presentación)
@app.route('/')
def hello_world():
    return "hola me llamo jofre y este es mi prueba de axamen de IA"

# Ruta de Chat con IA (Ahora permite GET para ver la web y POST para chatear)
@app.route('/ai', methods=['GET', 'POST'])
def ai():
    # 1. Si entras desde el navegador (GET), te mostramos la cajita de chat
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Chat IA</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 20px;">
            <h2>🤖 Chat de Prueba</h2>
            <input type="text" id="msg" placeholder="Escribe tu mensaje..." style="padding: 10px; width: 60%;">
            <button onclick="enviar()" style="padding: 10px;">Enviar</button>
            <p id="respuesta" style="margin-top: 20px; font-weight: bold; color: blue;"></p>

            <script>
                async function enviar() {
                    const texto = document.getElementById('msg').value;
                    const respDiv = document.getElementById('respuesta');
                    respDiv.innerText = "Pensando...";
                    
                    const res = await fetch('/ai', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({prompt: texto})
                    });
                    const data = await res.json();
                    respDiv.innerText = data.response;
                }
            </script>
        </body>
        </html>
        """
    
    # 2. Si es el sistema enviando el mensaje (POST)
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"response": "Por favor envía un prompt."})
    
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