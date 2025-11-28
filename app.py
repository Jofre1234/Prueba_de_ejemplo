from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

# Configuración para que los acentos y emojis se vean bien
app.config['JSON_AS_ASCII'] = False

# --- SOLUCIÓN AL ERROR ROJO DE CONSOLA ---
# Esto evita el error "(index):1 Failed to load resource: 404" del ícono
@app.route('/favicon.ico')
def favicon():
    return "", 204
# -----------------------------------------

@app.route('/', methods=['GET', 'POST'])
def home():
    # 1. SI ES UN HUMANO ENTRANDO POR NAVEGADOR (GET)
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Examen Jofre</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding: 20px; background: #f0f2f5; }
                .chat-container { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto; }
                h1 { color: #1a73e8; margin-bottom: 5px; }
                p.subtitle { color: #5f6368; margin-top: 0; }
                input { width: 70%; padding: 12px; border: 1px solid #dadce0; border-radius: 24px; outline: none; margin-top: 20px;}
                button { padding: 12px 24px; background: #1a73e8; color: white; border: none; border-radius: 24px; cursor: pointer; font-weight: bold; margin-left: 5px;}
                button:hover { background: #1557b0; }
                #respuesta { margin-top: 20px; min-height: 20px; color: #137333; font-weight: bold; font-size: 1.1em; }
            </style>
        </head>
        <body>
            <div class="chat-container">
                <h1>¡Hola! Soy Jofre Bedón</h1>
                <p class="subtitle">Prueba Final de IA 🤖</p>
                <hr style="border: 0; border-top: 1px solid #eee;">
                
                <input type="text" id="msg" placeholder="Escribe un mensaje aquí...">
                <button onclick="enviar()">Enviar</button>
                
                <p id="respuesta"></p>
            </div>

            <script>
                async function enviar() {
                    const txt = document.getElementById('msg').value;
                    const resp = document.getElementById('respuesta');
                    if (!txt) return;

                    resp.innerText = "Pensando...";
                    resp.style.color = "#666";
                    
                    try {
                        const res = await fetch('/', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({prompt: txt})
                        });
                        const data = await res.json();
                        resp.innerText = data.response;
                        resp.style.color = "#137333";
                    } catch (e) {
                        resp.innerText = "Error: " + e.message;
                        resp.style.color = "red";
                    }
                }
            </script>
        </body>
        </html>
        """
    
    # 2. SI ES EL CHAT ENVIANDO DATOS (POST)
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"response": "Por favor escribe algo."})
    return jsonify({"response": f"🤖 IA dice: {prompt}"})

# --- CONFIGURACIÓN DE SEGURIDAD PARA PRUEBAS ---
def run_tests():
    try:
        import pytest
        sys.exit(pytest.main([__file__]))
    except ImportError:
        print("Advertencia: pytest no está instalado, saltando pruebas.")

if __name__ == '__main__':
    if "test" in sys.argv:
        run_tests()
    else:
        # ¡ESTA LÍNEA ES LA CLAVE PARA QUE NO SALGA ERROR 404!
        # host='0.0.0.0' hace que la app sea visible desde fuera.
        app.run(debug=True, host='0.0.0.0', port=5000)