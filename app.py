from flask import Flask, request, jsonify
import secrets
import time

app = Flask(__name__)
application = app

key_data = {"key": None, "timestamp": None}

def generate_key():
    return secrets.token_hex(16)

def is_key_valid():
    if key_data["key"] and key_data["timestamp"]:
        return time.time() - key_data["timestamp"] <= 300
    return False

@app.route('/')
def home():
    if not is_key_valid():
        key_data["key"] = generate_key()
        key_data["timestamp"] = time.time()
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Access Key</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                position: relative;
                flex-direction: column;
                font-family: Arial, sans-serif;
                background: #f9f9f9;
            }}

            .author-banner {{
                position: absolute;
                top: 10px;
                left: 10px;
                background-color: #007BFF; /* azul */
                color: black;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 18px;
                user-select: none;
            }}

            .telegram-banner {{
                position: absolute;
                top: 10px;
                right: 10px;
                background-color: #007BFF; /* azul */
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
                user-select: none;
            }}
            .telegram-banner a {{
                color: black;
                text-decoration: none;
                font-weight: bold;
            }}
            .telegram-banner a:hover {{
                text-decoration: underline;
            }}

            .content {{
                text-align: center;
                margin-top: 20px;
            }}

            .key-container {{
                background-color: #007BFF; /* azul */
                padding: 12px 20px;
                border-radius: 8px;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                margin-top: 15px;
                user-select: none;
            }}

            .key-box {{
                background-color: white;
                color: black;
                font-size: 20px;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 320px;
                font-family: monospace;
                user-select: text;
                overflow-wrap: break-word;
            }}

            button.copy-btn {{
                background-color: black;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: background-color 0.3s ease;
                user-select: none;
            }}

            button.copy-btn:hover {{
                background-color: #333;
            }}

            .ad-banner {{
                width: 728px;
                height: 90px;
                background-color: #f4f4f4;
                padding: 10px;
                text-align: center;
                position: fixed;
                bottom: 0;
                box-shadow: 0 -2px 4px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div class="author-banner">Autor: Keno Venas</div>
        <div class="telegram-banner">
            <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank" rel="noopener noreferrer">Grupo do Telegram</a>
        </div>

        <div class="content">
            <h1>Access Key</h1>
            <div class="key-container">
                <div id="key-box" class="key-box">{key_data["key"]}</div>
                <button class="copy-btn" onclick="copyKey()">Copiar</button>
            </div>
        </div>

        <!-- Script da Hydro -->
        <script id="hydro_config" type="text/javascript">
            window.Hydro_tagId = "ab51bfd4-d078-4c04-a17b-ccfcfe865175";
        </script>
        <script id="hydro_script" src="https://track.hydro.online/"></script>

        <!-- anuncios -->
        <div class="ad-banner">
            <script type="text/javascript">
                atOptions = {{
                    'key' : '78713e6d4e36d5a549e9864674183de6',
                    'format' : 'iframe',
                    'height' : 90,
                    'width' : 728,
                    'params' : {{}}
                }};
            </script>
            <script type="text/javascript" src="//spiceoptimistic.com/78713e6d4e36d5a549e9864674183de6/invoke.js"></script>
        </div>
        <script type='text/javascript' src='//spiceoptimistic.com/1c/66/88/1c668878f3f644b95a54de17911c2ff5.js'></script>

        <script>
            function copyKey() {{
                const keyText = document.getElementById('key-box').innerText;
                navigator.clipboard.writeText(keyText).then(() => {{
                    alert('Chave copiada!');
                }}).catch(err => {{
                    alert('Erro ao copiar a chave.');
                }});
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    if 'key' in data:
        if data['key'] == key_data['key'] and is_key_valid():
            return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
