from flask import Flask, request, jsonify
import pyqrcode
from io import BytesIO
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seu_email@example.com'
app.config['MAIL_PASSWORD'] = 'sua_senha'
app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@example.com'

mail = Mail(app)

@app.route('/gerar_qrcode', methods=['POST'])
def gerar_qrcode():
    # Obtenha os dados da solicitação
    dados = request.get_json()
    valor = dados['valor']
    chave_pix = dados['chave_pix']
    email_usuario = dados['email_usuario']  # Adicione esta linha para obter o e-mail do usuário

    # Construa o payload do pagamento PIX
    payload = f"pixonline://{chave_pix}?amount={valor}"
    
    # Crie o código QR PIX
    qr_code = pyqrcode.create(payload)
    
    # Converta o código QR para uma imagem PNG
    buffer = BytesIO()
    qr_code.png(buffer, scale=5)
    buffer.seek(0)

    # Envie o e-mail de notificação para o usuário
    msg = Message('Pagamento PIX', recipients=[email_usuario])
    msg.body = f'Olá! Você recebeu uma solicitação de pagamento PIX no valor de R${valor}. Confirme a transação através do código QR PIX abaixo.'
    msg.attach('qrcode_pix.png', 'image/png', buffer.getvalue())
    mail.send(msg)

    # Retorne uma resposta de sucesso
    return jsonify({'mensagem': 'E-mail de notificação enviado com sucesso.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
