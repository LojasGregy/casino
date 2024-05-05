from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Simulação de dados de administrador (substitua isso com seus próprios dados)
admin_username = 'admin'
admin_password = 'senha_admin'

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect(url_for('add_game'))
        else:
            return 'Credenciais inválidas. Tente novamente.'
    return render_template('login.html')

# Rota para a página de adicionar jogo (requer autenticação de admin)
@app.route('/add_game')
def add_game():
    if session.get('logged_in'):
        return render_template('add_game.html')
    else:
        return redirect(url_for('login'))

# Rota para fazer logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
