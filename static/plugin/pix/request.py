import requests

dados_pagamento = {
    'valor': '100.00',
    'chave_pix': 'sua_chave_pix_aqui'
}

response = requests.post('http://localhost:5000/gerar_qrcode', json=dados_pagamento)

with open('qrcode_pix.png', 'wb') as f:
    f.write(response.content)
