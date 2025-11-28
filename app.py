from flask import Flask, request, jsonify
import pytest

app = Flask(__name__)

# Unificamos todo en la Ruta Principal '/'
# Ahora acepta GET (para ver la página) y POST (para el chat)
@app.route('/', methods=['GET', 'POST'])
def home():
    # 1. Si entras desde el navegador (GET), mostramos la web completa
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Examen Jofre</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="font-family: sans-serif; text-align: center; padding: 20px;">
            
            <!-- TU MENSAJE DE PRESENTACIÓN -->
            <h1 style="color: #333;">hola me llamo jofre y este es mi prueba de axamen de IA</h1>
            
            <hr style="margin: 20px auto; width: 50%;">

            <!-- CAJITA DE CHAT -->
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
                    
                    // Enviamos el mensaje a la misma ruta principal '/'
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
    
    # 2. Si es el sistema enviando el mensaje (POST - Chat)
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

    def test_home_get(client):
        # Probamos que al entrar se vea tu nombre y el chat
        response = client.get('/')
        assert response.status_code == 200
        assert "jofre".encode() in response.data
        assert "Chat de Prueba".encode() in response.data

    def test_chat_post(client):
        # Probamos que el chat responda en la misma ruta '/'
        response = client.post('/', json={"prompt": "Hola"})
        assert response.status_code == 200
        assert "Respuesta de IA".encode() in response.data

    pytest.main([__file__])


if __name__ == '__main__':
    import sys
    if "test" in sys.argv:
        run_tests()
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)