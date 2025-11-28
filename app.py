from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

# === RUTA PRINCIPAL (WEB Y CHAT) ===
@app.route('/', methods=['GET', 'POST'])
def home():
    # 1. Si es un humano (GET)
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Examen Jofre</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="font-family: sans-serif; text-align: center; padding: 20px;">
            <h1 style="color: #333;">¡Hola! Soy Jofre y esta es mi prueba de examen de IA</h1>
            <hr style="margin: 20px auto; width: 50%;">
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px; display: inline-block;">
                <h2>🤖 Chat de Prueba</h2>
                <input type="text" id="msg" placeholder="Escribe algo..." style="padding: 10px; width: 250px;">
                <button onclick="enviar()" style="padding: 10px; background: #007bff; color: white; border: none; cursor: pointer;">Enviar</button>
                <p id="respuesta" style="margin-top: 20px; font-weight: bold; color: blue; min-height: 20px;"></p>
            </div>
            <script>
                async function enviar() {
                    const texto = document.getElementById('msg').value;
                    const respDiv = document.getElementById('respuesta');
                    respDiv.innerText = "Pensando...";
                    const res = await fetch('/', {
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
    
    # 2. Si es el sistema (POST)
    try:
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"response": "Por favor envía un prompt."})
        return jsonify({"response": f"Respuesta de IA para: {prompt}"})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})


# === PRUEBAS ===
def run_tests():
    # Importar pytest AQUI ADENTRO para evitar errores si no está instalado
    import pytest
    
    @pytest.fixture
    def client():
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_home_get(client):
        response = client.get('/')
        assert response.status_code == 200

    pytest.main([__file__])


if __name__ == '__main__':
    if "test" in sys.argv:
        run_tests()
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)