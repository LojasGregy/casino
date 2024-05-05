from flask import Flask, request, jsonify
import pyqrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/gerar_qrcode', methods=['POST'])
def gerar_qrcode():
    # Obtenha os dados da solicitação
    dados = request.get_json()
    valor = dados['valor']
    chave_pix = dados['chave_pix']
    
    # Construa o payload do pagamento PIX
    payload = f"pixonline://{chave_pix}?amount={valor}"
    
    # Crie o código QR PIX
    qr_code = pyqrcode.create(payload)
    
    # Converta o código QR para uma imagem PNG
    buffer = BytesIO()
    qr_code.png(buffer, scale=5)
    buffer.seek(0)
    
    # Retorne o código QR como uma resposta
    return buffer.getvalue(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True)
