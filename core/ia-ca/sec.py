import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurar logging
logging.basicConfig(filename='ia.log', level=logging.INFO)

# Lista de usuários autorizados
usuarios_autorizados = {'usuario1': 'senha1', 'usuario2': 'senha2'}

# Função de autenticação
def autenticar_usuario(username, password):
    if username in usuarios_autorizados and usuarios_autorizados[username] == password:
        return True
    else:
        return False

# Middleware para validar a sessão do usuário
@app.before_request
def validar_sessao():
    # Verificar se a sessão é válida (exemplo simples)
    if 'username' not in session:
        return jsonify({'mensagem': 'Acesso não autorizado.'}), 401

# Rota para processar solicitações de login
@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    username = dados.get('username')
    password = dados.get('password')
    
    if autenticar_usuario(username, password):
        session['username'] = username
        logging.info(f'Usuário {username} fez login.')
        return jsonify({'mensagem': 'Login bem-sucedido.'}), 200
    else:
        logging.warning(f'Tentativa de login inválida para o usuário {username}.')
        return jsonify({'mensagem': 'Credenciais inválidas.'}), 401

# Rota para processar solicitações de logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    logging.info('Usuário fez logout.')
    return jsonify({'mensagem': 'Logout bem-sucedido.'}), 200

# Rota para processar solicitações de atividades suspeitas
@app.route('/atividade_suspeita', methods=['POST'])
def relatar_atividade_suspeita():
    dados = request.get_json()
    username = session.get('username')
    atividade = dados.get('atividade')

    if username:
        logging.warning(f'Atividade suspeita relatada pelo usuário {username}: {atividade}')
    else:
        logging.warning(f'Atividade suspeita relatada por um usuário não autenticado: {atividade}')

    return jsonify({'mensagem': 'Atividade suspeita relatada.'}), 200

if __name__ == '__main__':
    app.secret_key = 'chave_secreta_para_sessao'
    app.run(debug=True)
