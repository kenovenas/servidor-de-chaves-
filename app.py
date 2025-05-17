from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- IMPORTANTE PARA LIBERAR ACESSO EXTERNO
import secrets
import time

app = Flask(__name__)
CORS(app)  # <-- HABILITA CORS PARA PERMITIR ACESSO DE OUTRAS ORIGENS (EX: Tampermonkey)

# Dados da chave atual
key_data = {
    "key": None,
    "timestamp": None
}

# Gera uma nova chave aleatória
def generate_key():
    return secrets.token_hex(16)

# Verifica se a chave ainda é válida (duração: 5 minutos)
def is_key_valid():
    if key_data["key"] and key_data["timestamp"]:
        return time.time() - key_data["timestamp"] <= 300
    return False

@app.route('/')
def home():
    # Se não houver chave válida, gera uma nova
    if not is_key_valid():
        key_data["key"] = generate_key()
        key_data["timestamp"] = time.time()

    # Página HTML com a chave exibida
    return f'''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Acesse Key</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #ffffff;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .main-banner {{
                background-color: #007BFF;
                color: black;
                padding: 40px 30px;
                border-radius: 15px;
                text-align: center;
                width: 90%;
                max-width: 500px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}
            .main-banner h2 {{
                margin-top: 0;
                margin-bottom: 10px;
                font-size: 22px;
            }}
            .main-banner h3 {{
                margin-top: 10px;
                font-size: 20px;
            }}
            .key-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 15px 0;
            }}
            #key-box {{
                background-color: white;
                color: black;
                border: 2px solid #000;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 18px;
                min-width: 250px;
                user-select: all;
                margin-right: 10px;
            }}
            #copy-btn {{
                padding: 10px 15px;
                background-color: #ffffff;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }}
            .telegram-link {{
                margin-top: 20px;
                font-size: 16px;
            }}
            .telegram-link a {{
                color: black;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="main-banner">
            <h2>Autor: Keno Venas</h2>
            <h3>Acesse Key</h3>
            <div class="key-container">
                <div id="key-box">{key_data["key"]}</div>
                <button id="copy-btn">Copiar</button>
            </div>
            <div class="telegram-link">
                <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Entrar no Grupo do Telegram</a>
            </div>
        </div>

        <script>
            document.getElementById('copy-btn').addEventListener('click', function() {{
                const keyText = document.getElementById('key-box').textContent;
                const textarea = document.createElement('textarea');
                textarea.value = keyText;
                textarea.style.position = 'fixed';
                textarea.style.left = '-9999px';
                document.body.appendChild(textarea);
                textarea.select();
                try {{
                    document.execCommand('copy');
                    alert('Chave copiada!');
                }} catch (err) {{
                    alert('Erro ao copiar.');
                }}
                document.body.removeChild(textarea);
            }});
        </script>
    </body>
    </html>
    '''

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    if data and 'key' in data and data['key'] == key_data['key'] and is_key_valid():
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
