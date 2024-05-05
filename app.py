from flask import Flask, render_template, request
from flask import Flask, jsonify

app = Flask(__name__)

app = Flask(__name__)

# Simulação de dados do usuário (substitua isso com seus próprios dados)
user_data = {
    'username': 'joao123',
    'email': 'joao123@example.com',
    'saldo': 100.0,
    # Adicione mais campos conforme necessário
}

# Conteúdo da página inicial em Python
index_content = """
<h2>Bem-vindo ao Casino Online!</h2>
<p>Este é o conteúdo da página inicial.</p>
"""

# Conteúdo da página de administração em Python
admin_content = """
<h2>Página de Administração</h2>
<p>Este é o conteúdo da página de administração.</p>
"""
# Rota para obter os dados do usuário
@app.route('/get_user_data')
def get_user_data():
    # Retorna os dados do usuário no formato JSON
    return jsonify(user_data)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html', content=index_content)

# Rota para a página de administração
@app.route('/admin')
def admin():
    return render_template('admin.html', content=admin_content)

# Rota para usuários normais
@app.route('/user')
def user():
    user_content = """
    <h2>Página do Usuário Normal</h2>
    <p>Este é o conteúdo da página do usuário normal.</p>
    """
    return render_template('user.html', content=user_content)

# Rota para obter os dados do usuário
@app.route('/get_user_data')
def get_user_data():
    # Retorna os dados do usuário no formato JSON
    return jsonify(user_data)

# Rota para a página inicial
@app.route('/')
def index():
    return 'Página inicial'

# Rota para a página de administração
@app.route('/admin')
def admin():
    return 'Página de administração'

# Rota para a página do usuário
@app.route('/user')
def user():
    return 'Página do usuário'

if __name__ == '__main__':
    app.run(debug=True)
